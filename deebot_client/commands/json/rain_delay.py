
"""Rain delay commands."""
from collections.abc import Mapping
from typing import Any, Optional

from deebot_client.events import RainDelayEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus, SetCommand


class GetRainDelay(CommandWithMessageHandling, MessageBodyDataDict):
    """Get rain delay command."""

    name = "getInfo"

    def __init__(self) -> None:
        super().__init__(["getRainDelay"])

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        enable = False
        delay =  120

        v2_data = data.get("getRainDelay", None)

        if v2_data is not None:
            enable = bool(data["getRainDelay"]["data"]["enable"])
            delay = int(data["getRainDelay"]["data"]["delay"])
        else:
            enable = bool(data["enable"])
            delay = int(data["delay"])
        
        event_bus.notify(RainDelayEvent(enable,delay))
        return HandlingResult.success()

class SetRainDelay(SetCommand):
    """Set rain delay command."""

    name = "setRainDelay"
    get_command = GetRainDelay

    def __init__(self, enable: int | bool, delay:  Optional[int] = 120, **kwargs: Mapping[str, Any]) -> None:
        if isinstance(enable, bool):
            enable = 1 if enable else 0
        super().__init__({"enable":enable,"delay": delay}, **kwargs)
