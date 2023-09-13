"""Water info event module."""
from dataclasses import dataclass

from .base import Event

@dataclass(frozen=True)
class WifiInfoEvent(Event):
    """Wifi info event representation."""

    # None means no data available
    mac: str | None
    ssid: str | None
    rssi: int | None
    ip: str | None
