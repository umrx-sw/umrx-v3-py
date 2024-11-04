from array import array

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import I2CMode
from umrx_app_v3.mcu_board.commands.i2c import I2CConfigureCmd, I2CReadCmd


@pytest.mark.commands
def test_command_i2c_config(i2c_configure_command: I2CConfigureCmd) -> None:
    payload = i2c_configure_command.config()
    assert payload == array("B", (0xAA, 0x08, 0x01, 0x11, 0x01, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_i2c_config_set_speed(i2c_configure_command: I2CConfigureCmd) -> None:
    payload = i2c_configure_command.set_speed(I2CMode.STANDARD_MODE)
    assert payload == array("B", (0xAA, 0x08, 0x01, 0x09, 0x00, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_i2c_config_assemble(i2c_configure_command: I2CConfigureCmd) -> None:
    for idx, command in enumerate(i2c_configure_command.assemble()):
        if idx == 0:
            assert command == array("B", (0xAA, 0x08, 0x01, 0x11, 0x01, 0x00, 0x0D, 0x0A))
        if idx == 1:
            assert command == array("B", (0xAA, 0x08, 0x01, 0x09, 0x00, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_i2c_read_assemble(i2c_read_command: I2CReadCmd) -> None:
    payload = i2c_read_command.assemble(i2c_address=0x18, register_address=0x0, bytes_to_read=0x01)

    expected_payload = array(
        "B",
        (0xAA, 0x12, 0x02, 0x16, 0x01, 0x00, 0x01, 0x01, 0x00, 0x18, 0x00, 0x00, 0x01, 0x01, 0x00, 0x01, 0x0D, 0x0A),
    )

    assert payload == expected_payload
