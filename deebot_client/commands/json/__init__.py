"""Commands module."""
from deebot_client.command import Command, CommandMqttP2P

from .advanced_mode import GetAdvancedMode, SetAdvancedMode
from .battery import GetBattery
from .carpet import GetCarpetAutoFanBoost, SetCarpetAutoFanBoost
from .charge import Charge
from .charge_state import GetChargeState
from .clean import Clean, CleanArea, GetCleanInfo
from .clean_V2 import CleanV2, GetCleanInfoV2
from .clean_count import GetCleanCount, SetCleanCount
from .clean_logs import GetCleanLogs
from .clean_preference import GetCleanPreference, SetCleanPreference
from .common import JsonCommand
from .continuous_cleaning import GetContinuousCleaning, SetContinuousCleaning
from .error import GetError
from .fan_speed import GetFanSpeed, SetFanSpeed
from .life_span import GetLifeSpan, ResetLifeSpan, GetGoatLifeSpan
from .map import (
    GetCachedMapInfo,
    GetMajorMap,
    GetMapSet,
    GetMapSubSet,
    GetMapTrace,
    GetMinorMap,
)
from .multimap_state import GetMultimapState, SetMultimapState
from .play_sound import PlaySound
from .pos import GetPos
from .relocation import SetRelocationState
from .stats import GetStats, GetTotalStats
from .true_detect import GetTrueDetect, SetTrueDetect
from .volume import GetVolume, SetVolume
from .water_info import GetWaterInfo, SetWaterInfo
from .protect_state import GetProtectState
from .anim_protect import GetAnimProtect, SetAnimProtect
from .rain_delay import SetRainDelay,GetRainDelay
from .safe_protect import SetSafeProtect, GetSafeProtect
from .border_switch import SetBorderSwitch, GetBorderSwitch
from .recognization import SetRecognization, GetRecognization
from .child_lock import SetChildLock, GetChildLock
from .moveup_warning import SetMoveupWarning, GetMoveupWarning
from .cross_map_boarder_warning import SetCrossMapBorderWarning, GetCrossMapBorderWarning
from .cut_direction import SetCutDirection, GetCutDirection
from .wifi_info import GetWifiList
from .obstacle_height import GetObstacleHeight, SetObstacleHeight

# fmt: off
# ordered by file asc
_COMMANDS: list[type[JsonCommand]] = [
    GetAdvancedMode,
    SetAdvancedMode,

    GetBattery,

    GetCarpetAutoFanBoost,
    SetCarpetAutoFanBoost,

    GetCleanCount,
    SetCleanCount,

    GetCleanPreference,
    SetCleanPreference,

    Charge,

    GetChargeState,

    Clean,
    CleanArea,
    GetCleanInfo,

    CleanV2,
    GetCleanInfoV2,

    GetCleanLogs,

    GetContinuousCleaning,
    SetContinuousCleaning,

    GetError,

    GetFanSpeed,
    SetFanSpeed,

    GetLifeSpan,
    ResetLifeSpan,

    GetCachedMapInfo,
    GetMajorMap,
    GetMapSet,
    GetMapSubSet,
    GetMapTrace,
    GetMinorMap,

    GetMultimapState,
    SetMultimapState,

    PlaySound,

    GetPos,

    SetRelocationState,

    GetStats,
    GetTotalStats,

    GetTrueDetect,
    SetTrueDetect,

    GetVolume,
    SetVolume,

    GetWaterInfo,
    SetWaterInfo,

    GetProtectState,

    GetAnimProtect,
    SetAnimProtect,

    GetRainDelay,
    SetRainDelay,

    GetSafeProtect,
    SetSafeProtect,

    SetBorderSwitch,
    GetBorderSwitch,

    SetRecognization,
    GetRecognization,

    SetChildLock,
    GetChildLock,

    SetMoveupWarning,
    GetMoveupWarning,

    SetCrossMapBorderWarning,
    GetCrossMapBorderWarning,
    
    SetCutDirection, 
    GetCutDirection,

    GetWifiList,
    
    GetGoatLifeSpan,

    GetObstacleHeight,
    SetObstacleHeight,
]
# fmt: on

COMMANDS: dict[str, type[Command]] = {
    cmd.name: cmd for cmd in _COMMANDS  # type: ignore[misc]
}

COMMANDS_WITH_MQTT_P2P_HANDLING: dict[str, type[CommandMqttP2P]] = {
    cmd_name: cmd
    for (cmd_name, cmd) in COMMANDS.items()
    if issubclass(cmd, CommandMqttP2P)
}
