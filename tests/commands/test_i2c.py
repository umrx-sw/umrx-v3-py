from array import array

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import I2CBus, I2CMode
from umrx_app_v3.mcu_board.commands.command import CommandError
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
def test_command_i2c_config_parse(i2c_configure_command: I2CConfigureCmd) -> None:
    dummy_message = array("B", (0xCA, 0xFE))
    assert i2c_configure_command.parse(dummy_message) is None


@pytest.mark.commands
def test_command_i2c_read_assemble(i2c_read_command: I2CReadCmd) -> None:
    payload = i2c_read_command.assemble(i2c_address=0x18, register_address=0x0, bytes_to_read=0x01)

    expected_payload = array(
        "B",
        (0xAA, 0x12, 0x02, 0x16, 0x01, 0x00, 0x01, 0x01, 0x00, 0x18, 0x00, 0x00, 0x01, 0x01, 0x00, 0x01, 0x0D, 0x0A),
    )

    assert payload == expected_payload


@pytest.mark.commands
def test_command_i2c_read_parse_valid_response(i2c_read_command: I2CReadCmd) -> None:
    valid_resp = b"\xaa\x0e\x01\x00B\x16\x01\x00\x01\x01\x00\x1e\r\n"
    payload = i2c_read_command.parse(valid_resp)
    assert payload == array("B", (0x1E,))


@pytest.mark.commands
def test_command_i2c_read_parse_invalid_response(i2c_read_command: I2CReadCmd) -> None:
    invalid_resp_header = b"XD\x01\x00B\x16\x01\x00\x01\x01\x00\x1e\r\n"
    with pytest.raises(CommandError):
        i2c_read_command.parse(invalid_resp_header)

    invalid_resp_status = b"\xaa\x0e\x01\x03B\x16\x01\x00\x01\x01\x00\x1e\r\n"
    with pytest.raises(CommandError):
        i2c_read_command.parse(invalid_resp_status)

    invalid_resp_feature = b"\xaa\x0e\x01\x00B\x11\x01\x00\x01\x01\x00\x1e\r\n"
    with pytest.raises(CommandError):
        i2c_read_command.parse(invalid_resp_feature)


@pytest.mark.commands
def test_command_i2c_set_bus(i2c_read_command: I2CReadCmd) -> None:
    i2c_read_command.set_bus(I2CBus.BUS_I2C_1)
    assert i2c_read_command.DefaultI2CBus == I2CBus.BUS_I2C_1

    i2c_read_command.set_bus(I2CBus.BUS_I2C_0)
    assert i2c_read_command.DefaultI2CBus == I2CBus.BUS_I2C_0


@pytest.mark.commands
def test_command_i2c_read_parse_extended_read(i2c_read_command: I2CReadCmd) -> None:
    extended_read_resp = b"\xaa\x0f\x01\x00C\x16\x01\x00\x00\x02\x00\x1e\x1d\r\n"
    payload = i2c_read_command.parse(extended_read_resp)
    assert payload == array("B", (0x1E, 0x1D))
