from typing import Any
from unittest.mock import Mock

import pytest

from deebot_client.authentication import Authenticator
from deebot_client.commands.json import CleanV2, GetCleanInfoV2
from deebot_client.commands.json.clean_V2 import MowerAction
from deebot_client.events import StateEventV2
from deebot_client.events.event_bus import EventBus
from deebot_client.models import DeviceInfo, VacuumState
from tests.helpers import get_request_json

from . import assert_command, assert_set_command

@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {
				"getChargeState": {
					"code": 0,
					"msg": "ok",
					"data": {
						"isCharging": 0
					}
				},
				"getCleanInfo_V2": {
					"data": {
						"trigger": "none",
						"state": "idle"
					},
					"code": 0,
					"msg": "ok"
				},
            },
            StateEventV2(VacuumState.IDLE)
        ),
        (
            {
				"getChargeState": {
					"code": 0,
					"msg": "ok",
					"data": {
						"isCharging": 0,
					}
				},
				"getCleanInfo_V2": {
					"data": {
						"trigger": "none",
                        "cleanState": {
                            "motionState": "working"
                        },
						"state": "clean"
					},
					"code": 0,
					"msg": "ok"
				},
            },
            StateEventV2(VacuumState.CLEANING)
        ),
        (
            {
				"getChargeState": {
					"code": 0,
					"msg": "ok",
					"data": {
						"isCharging": 0,
					}
				},
				"getCleanInfo_V2": {
					"data": {
						"trigger": "none",
                        "cleanState": {
                            "motionState": "goCharging"
                        },
						"state": "clean"
					},
					"code": 0,
					"msg": "ok"
				},
            },
            StateEventV2(VacuumState.RETURNING)
        ),
        (
            {
				"getChargeState": {
					"code": 0,
					"msg": "ok",
					"data": {
						"isCharging": 1,
					}
				},
				"getCleanInfo_V2": {
					"data": {
						"trigger": "none",
						"state": "idle"
					},
					"code": 0,
					"msg": "ok"
				},
            },
            StateEventV2(VacuumState.DOCKED)
        ),
        (
            {
				"getChargeState": {
					"code": 0,
					"msg": "ok",
					"data": {
						"isCharging": 0,
					}
				},
				"getCleanInfo_V2": {
					"data": {
						"trigger": "alert",
						"state": "idle"
					},
					"code": 0,
					"msg": "ok"
				},
            },
            StateEventV2(VacuumState.ERROR)
        ),
        (
            {
				"getChargeState": {
					"code": 0,
					"msg": "ok",
					"data": {
						"isCharging": 0,
					}
				},
				"getCleanInfo_V2": {
					"data": {
						"trigger": "none",
                        "cleanState": {
                            "motionState": "pause"
                        },
						"state": "clean"
					},
					"code": 0,
					"msg": "ok"
				},
            },
            StateEventV2(VacuumState.PAUSED)
        ),
    ],
)
async def test_GetCutDirection(json: dict[str, Any], expected: StateEventV2) -> None:
    json = get_request_json(json)
    await assert_command(GetCleanInfoV2(), json, expected)



@pytest.mark.parametrize(
    "action, vacuum_state, expected",
    [
        (MowerAction.START, None, MowerAction.START),
        (MowerAction.START, VacuumState.PAUSED, MowerAction.RESUME),
        (MowerAction.START, VacuumState.DOCKED, MowerAction.START),
        (MowerAction.RESUME, None, MowerAction.RESUME),
        (MowerAction.RESUME, VacuumState.PAUSED, MowerAction.RESUME),
        (MowerAction.RESUME, VacuumState.DOCKED, MowerAction.START),
    ],
)
async def test_CleanV2_act(
    authenticator: Authenticator,
    device_info: DeviceInfo,
    action: MowerAction,
    vacuum_state: VacuumState | None,
    expected: MowerAction,
) -> None:
    event_bus = Mock(spec_set=EventBus)
    event_bus.get_last_event.return_value = (
        StateEventV2(vacuum_state) if vacuum_state is not None else None
    )
    command = CleanV2(action)

    await command.execute(authenticator, device_info, event_bus)

    assert isinstance(command._args, dict)
    assert command._args["act"] == expected.value
