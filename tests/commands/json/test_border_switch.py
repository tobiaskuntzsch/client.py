from typing import Any

import pytest

from deebot_client.commands.json import GetBorderSwitch, SetBorderSwitch
from deebot_client.events import BorderSwitchEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getBorderSwitch": {
					"data": {
						"enable": 1,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            BorderSwitchEvent(True)
        ),
        (
            {
				"getBorderSwitch": {
					"data": {
						"enable": 0,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            BorderSwitchEvent(False)
        ),
    ],
)
async def test_GetBorderSwitch(json: dict[str, Any], expected: BorderSwitchEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetBorderSwitch(), json, expected)


@pytest.mark.parametrize("value", [False,True])
async def test_SetBorderSwitch(value: bool) -> None:
    args = {
        "enable": 1 if value else 0
    }
    await assert_set_command(
        SetBorderSwitch(value), args, BorderSwitchEvent(value)
    )
