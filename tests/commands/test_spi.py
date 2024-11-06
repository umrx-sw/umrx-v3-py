from array import array

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, SPIBus, SPIMode, SPISpeed
from umrx_app_v3.mcu_board.commands.spi import SPIConfigureCmd, SPIReadCmd


@pytest.mark.commands
def test_command_spi_config(spi_configure_command: SPIConfigureCmd) -> None:
    payload = spi_configure_command.config()
    assert payload == array("B", (0xAA, 0x08, 0x01, 0x11, 0x00, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_spi_config_set_speed(spi_configure_command: SPIConfigureCmd) -> None:
    payload = spi_configure_command.set_speed(SPISpeed.MHz_5)
    assert payload == array("B", (0xAA, 0x0A, 0x01, 0x19, 0x00, 0x03, 0x08, 0x0C, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_spi_config_assemble(spi_configure_command: SPIConfigureCmd) -> None:
    for idx, command in enumerate(spi_configure_command.assemble()):
        if idx == 0:
            assert command == array("B", (0xAA, 0x08, 0x01, 0x11, 0x00, 0x00, 0x0D, 0x0A))
        if idx == 1:
            assert command == array("B", (0xAA, 0x0A, 0x01, 0x19, 0x00, 0x03, 0x08, 0x0C, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_spi_config_parse(spi_configure_command: SPIConfigureCmd) -> None:
    dummy_message = array("B", (0xCA, 0xFE))
    assert spi_configure_command.parse(dummy_message) is None


@pytest.mark.commands
def test_command_spi_set_bus(spi_configure_command: SPIConfigureCmd) -> None:
    spi_configure_command.set_bus(SPIBus.BUS_1)
    assert spi_configure_command.DefaultSPIBus == SPIBus.BUS_1

    spi_configure_command.set_bus(SPIBus.BUS_0)
    assert spi_configure_command.DefaultSPIBus == SPIBus.BUS_0


@pytest.mark.commands
def test_command_spi_set_mode(spi_configure_command: SPIConfigureCmd) -> None:
    spi_configure_command.set_mode(SPIMode.MODE_2)
    assert spi_configure_command.DefaultSPIMode == SPIMode.MODE_2

    spi_configure_command.set_mode(SPIMode.MODE_3)
    assert spi_configure_command.DefaultSPIMode == SPIMode.MODE_3


@pytest.mark.commands
def test_command_spi_read_assemble(spi_read_command: SPIReadCmd) -> None:
    payload = spi_read_command.assemble(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1, register_address=0x12, bytes_to_read=0x07
    )
    expected_payload = array(
        "B",
        (0xAA, 0x12, 0x02, 0x16, 0x01, 0x16, 0x01, 0x01, 0x00, 0x00, 0x92, 0x00, 0x07, 0x01, 0x00, 0x01, 0x0D, 0x0A),
    )

    assert payload == expected_payload

    payload = spi_read_command.assemble(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5, register_address=0x02, bytes_to_read=0x06
    )
    expected_payload = array(
        "B",
        (0xAA, 0x12, 0x02, 0x16, 0x01, 0x14, 0x01, 0x01, 0x00, 0x00, 0x82, 0x00, 0x06, 0x01, 0x00, 0x01, 0x0D, 0x0A),
    )

    assert payload == expected_payload


# @pytest.mark.commands
# def test_command_i2c_read_parse_valid_response(i2c_read_command: I2CReadCmd) -> None:
#     valid_resp = b"\xaa\x0e\x01\x00B\x16\x01\x00\x01\x01\x00\x1e\r\n"
#     payload = i2c_read_command.parse(valid_resp)
#     assert payload == array("B", (0x1E,))
#
#
# @pytest.mark.commands
# def test_command_i2c_read_parse_invalid_response(i2c_read_command: I2CReadCmd) -> None:
#     invalid_resp_header = b"XD\x01\x00B\x16\x01\x00\x01\x01\x00\x1e\r\n"
#     with pytest.raises(CommandError):
#         i2c_read_command.parse(invalid_resp_header)
#
#     invalid_resp_status = b"\xaa\x0e\x01\x03B\x16\x01\x00\x01\x01\x00\x1e\r\n"
#     with pytest.raises(CommandError):
#         i2c_read_command.parse(invalid_resp_status)
#
#     invalid_resp_feature = b"\xaa\x0e\x01\x00B\x11\x01\x00\x01\x01\x00\x1e\r\n"
#     with pytest.raises(CommandError):
#         i2c_read_command.parse(invalid_resp_feature)
#
#

#
#
# @pytest.mark.commands
# def test_command_i2c_read_parse_extended_read(i2c_read_command: I2CReadCmd) -> None:
#     extended_read_resp = b"\xaa\x0f\x01\x00C\x16\x01\x00\x00\x02\x00\x1e\x1d\r\n"
#     payload = i2c_read_command.parse(extended_read_resp)
#     assert payload == array("B", (0x1E, 0x1D))
