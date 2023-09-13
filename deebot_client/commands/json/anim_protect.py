"""Animal protect commands."""
from collections.abc import Mapping
from typing import Any, Optional

from deebot_client.events import AnimProtectEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus, SetCommand


class GetAnimProtect(CommandWithMessageHandling, MessageBodyDataDict):
    """Get animal protect command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__(["getAnimProtect"])

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        enable = False
        start =  ""
        end = ""

        v2_data = data.get("getAnimProtect", None)

        if v2_data is not None:
            enable = bool(data["getAnimProtect"]["data"]["enable"])
            start = str(data["getAnimProtect"]["data"]["start"])
            end = str(data["getAnimProtect"]["data"]["end"])
        else:
            enable = bool(data["enable"])
            start = str(data["start"])
            end = str(data["end"])
        
        event_bus.notify(AnimProtectEvent(enable,start,end))
        return HandlingResult.success()


class SetAnimProtect(SetCommand):
    """Set animal protect command."""

    name = "setAnimProtect"
    get_command = GetAnimProtect

    def __init__(self, enable: int | bool, start:  Optional[str] = "19:00" ,end:  Optional[str] = "7:00", **kwargs: Mapping[str, Any]) -> None:
        if isinstance(enable, bool):
            enable = 1 if enable else 0
        super().__init__({"enable":enable,"start": start,"end": end}, **kwargs)
