
"""Safe protect commands."""
from collections.abc import Mapping
from typing import Any, Optional

from deebot_client.events import SafeProtectEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus, SetCommand


class GetSafeProtect(CommandWithMessageHandling, MessageBodyDataDict):
    """Get safe protect protect command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__(["getSafeProtect"])

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        enable = False
        
        v2_data = data.get("getSafeProtect", None)

        if v2_data is not None:
            enable = bool(v2_data["data"]["enable"])
        else:
            enable = bool(data["enable"])
        
        event_bus.notify(SafeProtectEvent(enable))
        return HandlingResult.success()

class SetSafeProtect(SetCommand):
    """Set safe protect command."""

    name = "setSafeProtect"
    get_command = GetSafeProtect

    def __init__(self, enable: int | bool, **kwargs: Mapping[str, Any]) -> None:
        if isinstance(enable, bool):
            enable = 1 if enable else 0
        super().__init__({"enable":enable}, **kwargs)
