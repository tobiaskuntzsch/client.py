from typing import Any
from unittest.mock import Mock

from deebot_client.commands import CommandWithHandling
from deebot_client.events import Event
from deebot_client.events.event_bus import EventBus
from deebot_client.message import HandlingState


def assert_command_requested(
    command: CommandWithHandling, data: dict[str, Any], expected_event: Event
):
    event_bus = Mock(spec_set=EventBus)

    result = command.handle_requested(event_bus, data)

    assert result.state == HandlingState.SUCCESS
    event_bus.notify.assert_called_once_with(expected_event)
