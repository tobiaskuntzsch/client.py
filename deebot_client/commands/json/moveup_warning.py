
"""Moveup warning commands."""
from collections.abc import Mapping
from typing import Any, Optional

from deebot_client.events import MoveupWarningEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus, SetCommand


class GetMoveupWarning(CommandWithMessageHandling, MessageBodyDataDict):
    """Get moveup warning command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__(["getMoveupWarning"])

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        enable = False
        
        v2_data = data.get("getMoveupWarning", None)

        if v2_data is not None:
            enable = bool(v2_data["data"]["enable"])
        else:
            enable = bool(data["enable"])
        
        event_bus.notify(MoveupWarningEvent(enable))
        return HandlingResult.success()

class SetMoveupWarning(SetCommand):
    """Set moveup warning command."""

    name = "setMoveupWarning"
    get_command = GetMoveupWarning

    def __init__(self, enable: int | bool, **kwargs: Mapping[str, Any]) -> None:
        if isinstance(enable, bool):
            enable = 1 if enable else 0
        super().__init__({"enable":enable}, **kwargs)
