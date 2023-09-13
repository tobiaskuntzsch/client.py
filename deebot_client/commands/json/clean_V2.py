"""Clean/Mow V2 commands."""
from enum import Enum, unique
from typing import Any, Optional

from deebot_client.authentication import Authenticator
from deebot_client.command import CommandResult
from deebot_client.events import StateEventV2
from deebot_client.logging_filter import get_logger
from deebot_client.message import HandlingResult, MessageBodyDataDict
from deebot_client.models import DeviceInfo, VacuumState

from .common import CommandWithMessageHandling, EventBus, ExecuteCommand

_LOGGER = get_logger(__name__)


@unique
class MowerAction(str, Enum):
    """Enum class for all possible Mow actions."""

    START = "start"
    BORDER_CUT = "border_cut"
    PAUSE = "pause"
    RESUME = "resume"
    STOP = "stop"

@unique
class MowerMode(str, Enum):
    """Enum class for all possible Mow modes."""

    AUTO = "auto"
    BORDER = "border"


class CleanV2(ExecuteCommand):
    """Mow command."""

    name = "clean_V2"

    def __init__(self, action: MowerAction) -> None:
        super().__init__(self.__get_args(action))

    async def _execute(
        self, authenticator: Authenticator, device_info: DeviceInfo, event_bus: EventBus
    ) -> CommandResult:
        """Execute command."""
        state = event_bus.get_last_event(StateEventV2)
        if state and isinstance(self._args, dict):
            if (
                self._args["act"] == MowerAction.RESUME.value
                and state.state != VacuumState.PAUSED
            ):
                self._args = self.__get_args(MowerAction.START,device_info.did)
            elif (
                self._args["act"] == MowerAction.START.value
                and state.state == VacuumState.PAUSED
            ):
                self._args = self.__get_args(MowerAction.RESUME)


        return await super()._execute(authenticator, device_info, event_bus)

    @staticmethod
    def __get_args(action: MowerAction, did: Optional[str] = None) -> dict[str, Any]:
        args = {"act": action.value}
        if action == MowerAction.START:
            args["content"] = {}
            args["content"]["type"] = MowerMode.AUTO.value
        elif action == MowerAction.BORDER_CUT:
            args["act"] = "start"
            args["content"] = {}
            args["content"]["type"] = MowerMode.BORDER.value
            args["content"]["value"] = f"mid:{did}"
        elif action == MowerAction.STOP:
            args["content"] = {}
            args["content"]["type"] = ""
        return args


    
class GetCleanInfoV2(CommandWithMessageHandling, MessageBodyDataDict):
    """Get clean info v2 command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__(
            [
                "getCleanInfo_V2",
                "getChargeState",
            ]
        )

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """

        status: VacuumState | None = None
       
        cleaninfo_data = data["getCleanInfo_V2"]["data"]
        chargestate_data = data["getChargeState"]["data"]

        state = cleaninfo_data.get("state")
        
        if cleaninfo_data.get("trigger") == "alert":
            status = VacuumState.ERROR
        elif state == "clean":
            clean_state = cleaninfo_data.get("cleanState", {})
            motion_state = clean_state.get("motionState")
            if motion_state == "working":
                status = VacuumState.CLEANING
            elif motion_state == "pause":
                status = VacuumState.PAUSED
            elif motion_state == "goCharging":
                status = VacuumState.RETURNING

        elif state == "goCharging":
            status = VacuumState.RETURNING
        elif state == "idle":
            status = VacuumState.IDLE

        is_charging = chargestate_data.get("isCharging")
        if is_charging == 1:
            status = VacuumState.DOCKED            

        if status:
            event_bus.notify(StateEventV2(status))
            return HandlingResult.success()

        return HandlingResult.analyse()
