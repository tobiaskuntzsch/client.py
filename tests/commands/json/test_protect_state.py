from typing import Any

import pytest

from deebot_client.commands.json import GetProtectState
from deebot_client.events import ProtectStateEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getProtectState": {
					"data": {
						"isAnimProtect": 1,
                        "isEStop": 1,
                        "isLocked": 1,
                        "isRainDelay": 1,
                        "isRainProtect": 1,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            ProtectStateEvent(True,True,True,True,True)
        ),
        (
            {
				"getProtectState": {
					"data": {
                        "isAnimProtect": 0,
                        "isEStop": 0,
                        "isLocked": 0,
                        "isRainDelay": 0,
                        "isRainProtect": 0,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            ProtectStateEvent(False,False,False,False,False)
        ),
    ],
)
async def test_GetProtectState(json: dict[str, Any], expected: ProtectStateEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetProtectState(), json, expected)


