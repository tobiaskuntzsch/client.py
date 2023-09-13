from typing import Any

import pytest

from deebot_client.commands.json import GetWifiList
from deebot_client.events import WifiInfoEvent
from tests.helpers import get_request_json

from . import assert_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
                "mac": "xx:xx:xx:xx:xx:xx",
                "list": [
                    {
                        "ssid": "WLAN NAME",
                        "rssi": 99,
                        "ip": "192.168.0.1",
                        "mask": "255.255.252.0"
                    }
                ],
                "state": "ok"
            },
            WifiInfoEvent("xx:xx:xx:xx:xx:xx", "WLAN NAME", 99, "192.168.0.1")
        ),
    ],
)
async def test_GetWifiList(json: dict[str, Any], expected: WifiInfoEvent) -> None:
    json = get_request_json(json)
    await assert_command(GetWifiList(), json, expected)