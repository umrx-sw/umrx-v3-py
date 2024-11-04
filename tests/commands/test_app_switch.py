from array import array

import pytest

from umrx_app_v3.mcu_board.commands.app_switch import AppSwitchCmd


@pytest.mark.commands
def test_command_app_switch_assemble(app_switch_cmd: AppSwitchCmd) -> None:
    payload = app_switch_cmd.assemble(0xABCD)
    assert payload == array("B", (0xAA, 0x0A, 0x01, 0x30, 0x00, 0x00, 0xAB, 0xCD, 0x0D, 0x0A))

    payload = app_switch_cmd.assemble(0xCCDDBBAA)
    assert payload == array("B", (0xAA, 0x0A, 0x01, 0x30, 0xCC, 0xDD, 0xBB, 0xAA, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_app_switch_parse(app_switch_cmd: AppSwitchCmd) -> None:
    msg = array("B", (0xBA, 0xBE))
    assert app_switch_cmd.parse(msg) is None
