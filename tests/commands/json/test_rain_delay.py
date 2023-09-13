from typing import Any, Optional

import pytest

from deebot_client.commands.json import GetRainDelay, SetRainDelay
from deebot_client.events import RainDelayEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getRainDelay": {
					"data": {
						"enable": 1,
                        "delay": 120,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            RainDelayEvent(True,120)
        ),
        (
            {
				"getRainDelay": {
					"data": {
						"enable": 0,
                        "delay": 120,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            RainDelayEvent(False,120)
        ),
    ],
)
async def test_GetRainDelay(json: dict[str, Any], expected: RainDelayEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetRainDelay(), json, expected)


@pytest.mark.parametrize("value", [False,True])

async def test_SetRainDelay(value: bool, delay:  Optional[int] = 120) -> None:
    args = {
        "enable": 1 if value else 0,
        "delay": delay
    }
    await assert_set_command(
        SetRainDelay(value,delay), args, RainDelayEvent(value,delay)
    )
