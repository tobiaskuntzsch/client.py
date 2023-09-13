"""Events module."""

from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Optional

from ..events.base import Event
from ..models import Room, VacuumState
from ..util import DisplayNameIntEnum
from .fan_speed import FanSpeedEvent, FanSpeedLevel
from .map import (
    MajorMapEvent,
    MapSetEvent,
    MapSetType,
    MapSubsetEvent,
    MapTraceEvent,
    MinorMapEvent,
    Position,
    PositionsEvent,
    PositionType,
)
from .water_info import WaterAmount, WaterInfoEvent
from .wifi_info import WifiInfoEvent

@dataclass(frozen=True)
class BatteryEvent(Event):
    """Battery event representation."""

    value: int


class CleanJobStatus(DisplayNameIntEnum):
    """Enum of the different clean job status."""

    NO_STATUS = -2
    CLEANING = -1
    # below the identified stop_reason values
    FINISHED = 1
    MANUAL_STOPPED = 2, "manual stopped"
    FINISHED_WITH_WARNINGS = 3, "finished with warnings"


@dataclass(frozen=True)
class CleanLogEntry:
    """Clean log entry representation."""

    timestamp: int
    image_url: str
    type: str
    area: int
    stop_reason: CleanJobStatus
    duration: int  # in seconds


@dataclass(frozen=True)
class CleanLogEvent(Event):
    """Clean log event representation."""

    logs: list[CleanLogEntry]


@dataclass(frozen=True)
class CleanCountEvent(Event):
    """Clean count event representation."""

    count: int


@dataclass(frozen=True)
class CustomCommandEvent(Event):
    """Custom command event representation."""

    name: str
    response: dict[str, Any]


@dataclass(frozen=True)
class ErrorEvent(Event):
    """Error event representation."""

    code: int
    description: str | None


@unique
class LifeSpan(str, Enum):
    """Enum class for all possible life span components."""

    SIDE_BRUSH = "sideBrush"
    BRUSH = "brush"
    FILTER = "heap"


@unique
class GoatLifeSpan(str, Enum):
    """Enum class for all possible life span components."""

    BLADE = "blade"
    LENSBRUSH = "lensBrush"
    UWBCELL = "uwbCell"


@dataclass(frozen=True)
class NewUWBCellEvent(Event):
    """New cell event representation."""
    sn: str

@dataclass(frozen=True)
class LifeSpanEvent(Event):
    """Life span event representation."""

    type: LifeSpan
    percent: float
    remaining: int  # in minutes

@dataclass(frozen=True)
class GoatLifeSpanEvent(Event):
    """GoatLifeSpan span event representation."""

    type: GoatLifeSpan
    percent: float
    remaining: int  # in minutes  
    sn: str | None  

@dataclass(frozen=True)
class RoomsEvent(Event):
    """Room event representation."""

    rooms: list[Room]


@dataclass(frozen=True)
class StatsEvent(Event):
    """Stats event representation."""

    area: int | None
    time: int | None
    type: str | None


@dataclass(frozen=True)
class ReportStatsEvent(StatsEvent):
    """Report stats event representation."""

    cleaning_id: str
    status: CleanJobStatus
    content: list[int]


@dataclass(frozen=True)
class TotalStatsEvent(Event):
    """Total stats event representation."""

    area: int
    time: int
    cleanings: int


@dataclass(frozen=True)
class AvailabilityEvent(Event):
    """Availability event."""

    available: bool


@dataclass(frozen=True)
class StateEvent(Event):
    """State event representation."""

    state: VacuumState

@dataclass(frozen=True)
class StateEventV2(Event):
    """State event representation."""

    state: VacuumState

@dataclass(frozen=True)
class VolumeEvent(Event):
    """Volume event."""

    volume: int
    maximum: int | None


@dataclass(frozen=True)
class EnableEvent(Event):
    """Enabled event."""

    enable: bool


@dataclass(frozen=True)
class AdvancedModeEvent(EnableEvent):
    """Advanced mode event."""


@dataclass(frozen=True)
class ContinuousCleaningEvent(EnableEvent):
    """Continuous cleaning event."""


@dataclass(frozen=True)
class CarpetAutoFanBoostEvent(EnableEvent):
    """Carpet pressure event."""


@dataclass(frozen=True)
class CleanPreferenceEvent(EnableEvent):
    """CleanPreference event."""


@dataclass(frozen=True)
class MultimapStateEvent(EnableEvent):
    """Multimap state event."""


@dataclass(frozen=True)
class TrueDetectEvent(EnableEvent):
    """TrueDetect event."""


@dataclass(frozen=True)
class ObstacleHeightEvent(Event):
    """Obstacle height event representation."""

    # None means no data available
    level: int | None

@dataclass(frozen=True)
class CutDirectionEvent(Event):
    """Cut direction  event representation."""

    # None means no data available
    angle: int | None

@dataclass(frozen=True)
class ProtectStateEvent(Event):
    """Protect state event representation."""

    # None means no data available
    is_anim_protect: bool | None
    is_e_stop: bool | None
    is_locked: bool | None
    is_rain_delay: bool | None
    is_rain_protect: bool | None

@dataclass(frozen=True)
class AnimProtectEvent(Event):
    """Animal protect event representation."""

    # None means no data available
    enable: bool
    start: str | None
    end: str | None


@dataclass(frozen=True)
class RainDelayEvent(Event):
    """Rain delay event representation."""

    # None means no data available
    enable: bool
    delay: int | None


@dataclass(frozen=True)
class SafeProtectEvent(Event):
    """Safe protect event representation."""

    # None means no data available
    enable: bool

@dataclass(frozen=True)
class BorderSwitchEvent(Event):
    """Border switch event representation."""

    # None means no data available
    enable: bool

@dataclass(frozen=True)
class RecognizationEvent(Event):
    """Recognization event representation."""

    # None means no data available
    enable: bool

@dataclass(frozen=True)
class ChildLockEvent(Event):
    """Child lock event representation."""

    # None means no data available
    enable: bool

@dataclass(frozen=True)
class MoveupWarningEvent(Event):
    """Moveup warning event representation."""

    # None means no data available
    enable: bool

@dataclass(frozen=True)
class CrossMapBorderWarningEvent(Event):
    """Cross map border warning event representation."""

    # None means no data available
    enable: bool