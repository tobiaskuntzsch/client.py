from typing import Any

import pytest

from deebot_client.commands.json import GetSafeProtect, SetSafeProtect
from deebot_client.events import SafeProtectEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getSafeProtect": {
					"data": {
						"enable": 1,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            SafeProtectEvent(True)
        ),
        (
            {
				"getSafeProtect": {
					"data": {
						"enable": 0,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            SafeProtectEvent(False)
        ),
    ],
)
async def test_GetSafeProtect(json: dict[str, Any], expected: SafeProtectEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetSafeProtect(), json, expected)


@pytest.mark.parametrize("value", [False,True])
async def test_SetSafeProtect(value: bool) -> None:
    args = {
        "enable": 1 if value else 0
    }
    await assert_set_command(
        SetSafeProtect(value), args, SafeProtectEvent(value)
    )
