
"""Cross map border warning commands."""
from collections.abc import Mapping
from typing import Any, Optional

from deebot_client.events import CrossMapBorderWarningEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus, SetCommand


class GetCrossMapBorderWarning(CommandWithMessageHandling, MessageBodyDataDict):
    """Get cross map border warning command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__(["getCrossMapBorderWarning"])

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        enable = False
        
        v2_data = data.get("getCrossMapBorderWarning", None)

        if v2_data is not None:
            enable = bool(v2_data["data"]["enable"])
        else:
            enable = bool(data["enable"])
        
        event_bus.notify(CrossMapBorderWarningEvent(enable))
        return HandlingResult.success()

class SetCrossMapBorderWarning(SetCommand):
    """Set cross map border warning command."""

    name = "setCrossMapBorderWarning"
    get_command = GetCrossMapBorderWarning

    def __init__(self, enable: int | bool, **kwargs: Mapping[str, Any]) -> None:
        if isinstance(enable, bool):
            enable = 1 if enable else 0
        super().__init__({"enable":enable}, **kwargs)
