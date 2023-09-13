from typing import Any

import pytest

from deebot_client.commands.json import GetCrossMapBorderWarning, SetCrossMapBorderWarning
from deebot_client.events import CrossMapBorderWarningEvent
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getCrossMapBorderWarning": {
					"data": {
						"enable": 1,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            CrossMapBorderWarningEvent(True)
        ),
        (
            {
				"getCrossMapBorderWarning": {
					"data": {
						"enable": 0,
					},
					"code": 0,
					"msg": "ok"
				}
            },
            CrossMapBorderWarningEvent(False)
        ),
    ],
)
async def test_GetCrossMapBorderWarning(json: dict[str, Any], expected: CrossMapBorderWarningEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetCrossMapBorderWarning(), json, expected)


@pytest.mark.parametrize("value", [False,True])
async def test_SetCrossMapBorderWarning(value: bool) -> None:
    args = {
        "enable": 1 if value else 0
    }
    await assert_set_command(
        SetCrossMapBorderWarning(value), args, CrossMapBorderWarningEvent(value)
    )
