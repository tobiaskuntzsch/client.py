
"""Cut direction commands."""
from collections.abc import Mapping
from typing import Any, Optional

from deebot_client.events import CutDirectionEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus, SetCommand


class GetCutDirection(CommandWithMessageHandling, MessageBodyDataDict):
    """Get cut direction command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__(["getCutDirection"])

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        angle = 90
        
        v2_data = data.get("getCutDirection", None)

        if v2_data is not None:
            angle = int(v2_data["data"]["angle"])
        else:
            angle = int(data["angle"])
        
        event_bus.notify(CutDirectionEvent(angle))
        return HandlingResult.success()

class SetCutDirection(SetCommand):
    """Set cut direction command."""

    name = "setCutDirection"
    get_command = GetCutDirection

    def __init__(self, angle: int | bool, **kwargs: Mapping[str, Any]) -> None:
        super().__init__({"angle":angle}, **kwargs)
