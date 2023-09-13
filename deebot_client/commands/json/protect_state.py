"""Protect state commands."""
from typing import Any

from deebot_client.events import ProtectStateEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus


class GetProtectState(CommandWithMessageHandling, MessageBodyDataDict):
    """Get protect state command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__([
            "getProtectState",
        ])

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        is_anim_protect = data["getProtectState"]["data"]["isAnimProtect"]
        is_e_stop = data["getProtectState"]["data"]["isEStop"]
        is_locked = data["getProtectState"]["data"]["isLocked"]
        is_rain_delay = data["getProtectState"]["data"]["isRainDelay"]
        is_rain_protect = data["getProtectState"]["data"]["isRainProtect"]

        event_bus.notify(ProtectStateEvent(is_anim_protect,is_e_stop,is_locked,is_rain_delay,is_rain_protect))
        return HandlingResult.success()
