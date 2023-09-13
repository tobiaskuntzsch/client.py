from typing import Any

import pytest

from deebot_client.commands.json import GetObstacleHeight, SetObstacleHeight
from deebot_client.events import ObstacleHeightEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getObstacleHeight": {
					"data": {
						"level": 1,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            ObstacleHeightEvent(1)
        ),
        (
            {
				"getObstacleHeight": {
					"data": {
						"level": 2,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            ObstacleHeightEvent(2)
        ),
        (
            {
				"getObstacleHeight": {
					"data": {
						"level": 3,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            ObstacleHeightEvent(3)
        ),
    ],
)
async def test_GetObstacleHeight(json: dict[str, Any], expected: ObstacleHeightEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetObstacleHeight(), json, expected)


@pytest.mark.parametrize("value", [1,2,3])
async def test_SetObstacleHeight(value: int) -> None:
    args = {
        "level": value
    }
    await assert_set_command(
        SetObstacleHeight(value), args, ObstacleHeightEvent(value)
    )
