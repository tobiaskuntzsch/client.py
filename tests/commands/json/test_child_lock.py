from typing import Any

import pytest

from deebot_client.commands.json import GetChildLock, SetChildLock
from deebot_client.events import ChildLockEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getChildLock": {
					"data": {
						"on": 1,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            ChildLockEvent(True)
        ),
        (
            {
				"getChildLock": {
					"data": {
						"on": 0,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            ChildLockEvent(False)
        ),
    ],
)
async def test_GetChildLock(json: dict[str, Any], expected: ChildLockEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetChildLock(), json, expected)


@pytest.mark.parametrize("value", [False,True])
async def test_SetChildLock(value: bool) -> None:
    args = {
        "on": 1 if value else 0
    }
    await assert_set_command(
        SetChildLock(value), args, ChildLockEvent(value)
    )
