from array import array

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import I2CMode
from umrx_app_v3.mcu_board.commands.i2c import I2CConfigureCmd


@pytest.mark.commands
def test_command_i2c_config(i2c_configure_command: I2CConfigureCmd) -> None:
    payload = i2c_configure_command.config()
    assert payload == array("B", (0xAA, 0x08, 0x01, 0x11, 0x01, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_i2c_set_speed(i2c_configure_command: I2CConfigureCmd) -> None:
    payload = i2c_configure_command.set_speed(I2CMode.STANDARD_MODE)
    assert payload == array("B", (0xAA, 0x08, 0x01, 0x09, 0x00, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_assemble(i2c_configure_command: I2CConfigureCmd) -> None:
    for idx, command in enumerate(i2c_configure_command.assemble()):
        if idx == 0:
            assert command == array("B", (0xAA, 0x08, 0x01, 0x11, 0x01, 0x00, 0x0D, 0x0A))
        if idx == 1:
            assert command == array("B", (0xAA, 0x08, 0x01, 0x09, 0x00, 0x00, 0x0D, 0x0A))
