from typing import Any

import pytest

from deebot_client.commands.json import GetLifeSpan, GetGoatLifeSpan
from deebot_client.events import LifeSpan, LifeSpanEvent, GoatLifeSpan, GoatLifeSpanEvent
from tests.helpers import get_request_json

from . import assert_command


@pytest.mark.parametrize(
    "json, expected",
    [
        (
            get_request_json(
                [
                    {"type": "sideBrush", "left": 8977, "total": 9000},
                    {"type": "brush", "left": 17979, "total": 18000},
                    {"type": "heap", "left": 7179, "total": 7200},
                ]
            ),
            [
                LifeSpanEvent(LifeSpan.SIDE_BRUSH, 99.74, 8977),
                LifeSpanEvent(LifeSpan.BRUSH, 99.88, 17979),
                LifeSpanEvent(LifeSpan.FILTER, 99.71, 7179),
            ],
        ),
    ],
)

async def test_GetLifeSpan(json: dict[str, Any], expected: list[LifeSpanEvent]) -> None:
    await assert_command(GetLifeSpan(), json, expected)

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            get_request_json(
                [
                    {"type": "blade", "left": 1000, "total": 1000,"sn":""},
                    {"type": "lensBrush", "left": 1000, "total": 1000,"sn":""},
                    {"type": "uwbCell", "left": 1000, "total": 1000,"sn":"3Cxxx"},
                ]
            ),
            [
                GoatLifeSpanEvent(GoatLifeSpan.BLADE, 100.00, 1000,""),
                GoatLifeSpanEvent(GoatLifeSpan.LENSBRUSH, 100.00, 1000,""),
                GoatLifeSpanEvent(GoatLifeSpan.UWBCELL, 100.00, 1000,"3Cxxx"),
            ],
        ),
    ],
)

async def test_GetGoatLifeSpan(json: dict[str, Any], expected: list[GoatLifeSpanEvent]) -> None:
    await assert_command(GetGoatLifeSpan(), json, expected)