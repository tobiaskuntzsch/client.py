"""Mower protect state commands."""
from typing import Any

from deebot_client.events.wifi_info import WifiInfoEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, EventBus


class GetWifiList(CommandWithMessageHandling, MessageBodyDataDict):
    """Get mower protect state command."""

    name = "getWifiList"

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        
        mac = data["mac"]
        ssid = data["list"][0]["ssid"]
        rssi = data["list"][0]["rssi"]
        ip = data["list"][0]["ip"]

        event_bus.notify(WifiInfoEvent(mac,ssid,rssi,ip))
        return HandlingResult.success()
