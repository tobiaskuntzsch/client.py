from typing import Any

import pytest

from deebot_client.commands.json import GetRecognization, SetRecognization
from deebot_client.events import RecognizationEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getRecognization": {
					"data": {
						"state": 1,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            RecognizationEvent(True)
        ),
        (
            {
				"getRecognization": {
					"data": {
						"state": 0,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            RecognizationEvent(False)
        ),
    ],
)
async def test_GetRecognization(json: dict[str, Any], expected: RecognizationEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetRecognization(), json, expected)


@pytest.mark.parametrize("value", [False,True])
async def test_SetRecognization(value: bool) -> None:
    args = {
        "state": 1 if value else 0
    }
    await assert_set_command(
        SetRecognization(value), args, RecognizationEvent(value)
    )
