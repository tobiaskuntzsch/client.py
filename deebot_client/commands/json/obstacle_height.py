
"""Obstacle height commands."""
from collections.abc import Mapping
from typing import Any, Optional

from deebot_client.events import ObstacleHeightEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus, SetCommand


class GetObstacleHeight(CommandWithMessageHandling, MessageBodyDataDict):
    """Get obstacle height protect command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__(["getObstacleHeight"])

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        level = 1
        
        v2_data = data.get("getObstacleHeight", None)

        if v2_data is not None:
            level = int(v2_data["data"]["level"])
        else:
            level = int(data["level"])
        
        event_bus.notify(ObstacleHeightEvent(level))
        return HandlingResult.success()

class SetObstacleHeight(SetCommand):
    """Set obstacle height command."""

    name = "setObstacleHeight"
    get_command = GetObstacleHeight

    def __init__(self, level: int | bool, **kwargs: Mapping[str, Any]) -> None:
        super().__init__({"level":level}, **kwargs)
