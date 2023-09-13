"""Vacuum bot module."""
import asyncio
import json
from collections.abc import Callable
from contextlib import suppress
from datetime import datetime
from typing import Any, Final,TypeVar

from deebot_client.commands.json.battery import GetBattery
from deebot_client.commands.json.life_span import GetGoatLifeSpan

from deebot_client.mqtt_client import MqttClient, SubscriberInfo

from .authentication import Authenticator
from .command import Command
from .events import (
    Event,
    AvailabilityEvent,
    CleanLogEvent,
    CustomCommandEvent,
    LifeSpanEvent,
    GoatLifeSpanEvent,
    GoatLifeSpan,
    PositionsEvent,
    PositionType,
    StateEvent,
    StateEventV2,
    StatsEvent,
    TotalStatsEvent,
    NewUWBCellEvent,
)
from .events.event_bus import EventBus
from .logging_filter import get_logger
from .map import Map
from .messages import get_message
from .models import DeviceInfo, VacuumState

_LOGGER = get_logger(__name__)
_AVAILABLE_CHECK_INTERVAL = 60

T = TypeVar("T", bound=Event)

class VacuumBot:
    """Vacuum bot representation."""

    def __init__(
        self,
        device_info: DeviceInfo,
        authenticator: Authenticator,
    ):
        self.device_info: Final[DeviceInfo] = device_info
        
        self._authenticator = authenticator

        self._semaphore = asyncio.Semaphore(3)
        
        self._last_time_available: datetime = datetime.now()
        self._available_task: asyncio.Task | None = None
        self._unsubscribe: Callable[[], None] | None = None
        self._state:  StateEvent | None = None

        self.fw_version: str | None = None
        self.events: Final[EventBus] = EventBus(self.execute_command)

        self.map: Final[Map] = Map(self.execute_command, self.events)

        self.uwbCells = []
        self.is_goat = (device_info.device_name == "GOAT")
        self._state_event_type: StateEvent | None = None
        self._life_span_event_type: LifeSpanEvent | None = None
        self._on_pos_refresh_event: StateEvent(VacuumState.DOCKED)  | None = None
        
        if self.is_goat:
            self._state_event_type: StateEventV2 | None = None
            self._life_span_event_type: GoatLifeSpanEvent | None = None
            self._on_pos_refresh_event: StateEventV2(VacuumState.DOCKED)  | None = None
            self._state:  StateEventV2 | None = None

            async def on_uwbcell_event(event: GoatLifeSpanEvent) -> None:
                if event.type == GoatLifeSpan.UWBCELL:
                    if not event.sn in self.uwbCells:
                        self.uwbCells.append(event.sn)
                        self.events.notify(NewUWBCellEvent(event.sn))
                        
            self.events.subscribe(GoatLifeSpanEvent, on_uwbcell_event)
            
            asyncio.create_task(self._uwbCell_task_worker())


        async def on_state(event: self._state) -> None:
            if event.state == StateEvent:
                self.events.request_refresh(CleanLogEvent)
                self.events.request_refresh(TotalStatsEvent)

        self.events.subscribe(self._state, on_state)
        
        async def on_pos(event: PositionsEvent) -> None:

            if self._state == self._on_pos_refresh_event:
                return

            deebot = next(p for p in event.positions if p.type == PositionType.DEEBOT)

            if deebot:
                on_charger = filter(
                    lambda p: p.type == PositionType.CHARGER
                    and p.x == deebot.x
                    and p.y == deebot.y,
                    event.positions,
                )
                if on_charger:
                    # deebot on charger so the status should be docked... Checking
                    self.events.request_refresh(self._on_pos_refresh_event) 
                         
        self.events.subscribe(PositionsEvent, on_pos) 

        async def on_stats(_: StatsEvent) -> None:
            self.events.request_refresh(self._life_span_event_type)

        self.events.subscribe(StatsEvent, on_stats)       

        async def on_custom_command(event: CustomCommandEvent) -> None:
            self._handle_message(event.name, event.response)

        self.events.subscribe(CustomCommandEvent, on_custom_command)

    async def _uwbCell_task_worker(self) -> None:
        try:
            await self._execute_command(GetGoatLifeSpan())
        except Exception:  # pylint: disable=broad-exception-caught
            _LOGGER.debug(
                "An exception occurred during uwbCell load",
                exc_info=True,
            )

    async def execute_command(self, command: Command) -> None:
        """Execute given command."""
        await self._execute_command(command)
       
    async def initialize(self, client: MqttClient) -> None:
        """Initialize vacumm bot, which includes MQTT-subscription and starting the available check."""
        if self._unsubscribe is None:
            self._unsubscribe = await client.subscribe(
                SubscriberInfo(self.device_info, self.events, self._handle_message)
            )

        if self._available_task is None or self._available_task.done():
            self._available_task = asyncio.create_task(self._available_task_worker())

    async def teardown(self) -> None:
        """Tear down bot including stopping task and unsubscribing."""
        if self._unsubscribe:
            self._unsubscribe()
            self._unsubscribe = None

        if self._available_task and self._available_task.cancel():
            with suppress(asyncio.CancelledError):
                await self._available_task

        await self.events.teardown()
        await self.map.teardown()

    async def _available_task_worker(self) -> None:

        while True:
            if (datetime.now() - self._last_time_available).total_seconds() > (
                _AVAILABLE_CHECK_INTERVAL - 1
            ):
                # request GetBattery to check availability
                try:
                    self._set_available(await self._execute_command(GetBattery(True)))
                except Exception:  # pylint: disable=broad-exception-caught
                    _LOGGER.debug(
                        "An exception occurred during the available check",
                        exc_info=True,
                    )

            await asyncio.sleep(_AVAILABLE_CHECK_INTERVAL)

    async def _execute_command(self, command: Command) -> bool:
        """Execute given command."""
        async with self._semaphore:
            if await command.execute(
                self._authenticator, self.device_info, self.events
            ):
                self._set_available(True)
                return True

        return False

    def _set_available(self, available: bool) -> None:
        """Set available."""
        if available:
            self._last_time_available = datetime.now()

        self.events.notify(AvailabilityEvent(available))

    def _handle_message(
        self, message_name: str, message_data: str | bytes | bytearray | dict[str, Any]
    ) -> None:
        """Handle the given message.

        :param message_name: message name
        :param message_data: message data
        :return: None
        """
        self._set_available(True)

        try:
            _LOGGER.debug("Try to handle message %s: %s", message_name, message_data)

            if message := get_message(message_name, self.device_info.data_type):
                if isinstance(message_data, dict):
                    data = message_data
                else:
                    data = json.loads(message_data)

                fw_version = data.get("header", {}).get("fwVer", None)
                if fw_version:
                    self.fw_version = fw_version

                message.handle(self.events, data)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.error(
                "An exception occurred during handling message", exc_info=True
            )
