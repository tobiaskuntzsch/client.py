from typing import Any

import pytest

from deebot_client.commands.json import GetMoveupWarning, SetMoveupWarning
from deebot_client.events import MoveupWarningEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getMoveupWarning": {
					"data": {
						"enable": 1,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            MoveupWarningEvent(True)
        ),
        (
            {
				"getMoveupWarning": {
					"data": {
						"enable": 0,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            MoveupWarningEvent(False)
        ),
    ],
)
async def test_GetMoveupWarning(json: dict[str, Any], expected: MoveupWarningEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetMoveupWarning(), json, expected)


@pytest.mark.parametrize("value", [False,True])
async def test_SetMoveupWarning(value: bool) -> None:
    args = {
        "enable": 1 if value else 0
    }
    await assert_set_command(
        SetMoveupWarning(value), args, MoveupWarningEvent(value)
    )
