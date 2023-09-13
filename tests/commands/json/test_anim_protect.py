from typing import Any, Optional

import pytest

from deebot_client.commands.json import GetAnimProtect, SetAnimProtect
from deebot_client.events import AnimProtectEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getAnimProtect": {
					"data": {
						"enable": 1,
						"start": "19:0",
						"end": "7:0"
					},
					"code": 0,
					"msg": "ok"
				}
            },
            AnimProtectEvent(True,"19:0","7:0")
        ),
    ],
)
async def test_GetAnimProtect(json: dict[str, Any], expected: AnimProtectEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetAnimProtect(), json, expected)


@pytest.mark.parametrize("value", [False,True])
async def test_SetAnimProtect(value: bool, start:  Optional[str] = "19:00" ,end:  Optional[str] = "7:00") -> None:
    args = {
        "enable": 1 if value else 0,
        "start": start,
        "end": end
    }
    await assert_set_command(
        SetAnimProtect(value,start,end), args, AnimProtectEvent(value,start,end)
    )
