
"""Child lock commands."""
from collections.abc import Mapping
from typing import Any, Optional

from deebot_client.events import ChildLockEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus, SetCommand


class GetChildLock(CommandWithMessageHandling, MessageBodyDataDict):
    """Get child lock command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__(["getChildLock"])

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        enable = False
        
        v2_data = data.get("getChildLock", None)

        if v2_data is not None:
            enable = bool(v2_data["data"]["on"])
        else:
            enable = bool(data["on"])
        
        event_bus.notify(ChildLockEvent(enable))
        return HandlingResult.success()

class SetChildLock(SetCommand):
    """Set child lock command."""

    name = "setChildLock"
    get_command = GetChildLock

    def __init__(self, enable: int | bool, **kwargs: Mapping[str, Any]) -> None:
        if isinstance(enable, bool):
            enable = 1 if enable else 0
        super().__init__({"on":enable}, **kwargs)
