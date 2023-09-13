from typing import Any

import pytest

from deebot_client.commands.json import GetCutDirection, SetCutDirection
from deebot_client.events import CutDirectionEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getCutDirection": {
					"data": {
						"angle": 90,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            CutDirectionEvent(90)
        ),
        (
            {
				"getCutDirection": {
					"data": {
						"angle": 45,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            CutDirectionEvent(45)
        ),
        (
            {
				"getCutDirection": {
					"data": {
						"angle": 0,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            CutDirectionEvent(0)
        ),
    ],
)
async def test_GetCutDirection(json: dict[str, Any], expected: CutDirectionEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetCutDirection(), json, expected)


@pytest.mark.parametrize("value", [0,45,90])
async def test_SetCutDirection(value: int) -> None:
    args = {
        "angle": value
    }
    await assert_set_command(
        SetCutDirection(value), args, CutDirectionEvent(value)
    )
