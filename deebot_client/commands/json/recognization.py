
"""Recognization commands."""
from collections.abc import Mapping
from typing import Any, Optional

from deebot_client.events import RecognizationEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus, SetCommand


class GetRecognization(CommandWithMessageHandling, MessageBodyDataDict):
    """Get recognization command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__(["getRecognization"])

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        enable = False
        
        v2_data = data.get("getRecognization", None)

        if v2_data is not None:
            enable = bool(v2_data["data"]["state"])
        else:
            enable = bool(data["state"])
        
        event_bus.notify(RecognizationEvent(enable))
        return HandlingResult.success()

class SetRecognization(SetCommand):
    """Set recognization command."""

    name = "setRecognization"
    get_command = GetRecognization

    def __init__(self, enable: int | bool, **kwargs: Mapping[str, Any]) -> None:
        if isinstance(enable, bool):
            enable = 1 if enable else 0
        super().__init__({"state":enable}, **kwargs)
