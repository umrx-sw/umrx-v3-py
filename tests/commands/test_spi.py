from array import array

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, SPIBus, SPIMode, SPISpeed
from umrx_app_v3.mcu_board.commands.command import CommandError
from umrx_app_v3.mcu_board.commands.spi import SPIConfigureCmd, SPIReadCmd, SPIWriteCmd


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
    with pytest.raises(CommandError):
        spi_configure_command.parse(dummy_message)

    good_response = array("B", [170, 12, 1, 0, 65, 25, 1, 3, 8, 12, 13, 10])

    assert spi_configure_command.parse(good_response) is None


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


@pytest.mark.commands
def test_command_spi_read_parse_valid_response(spi_read_command: SPIReadCmd) -> None:
    valid_resp = array(
        "B",
        (
            0xAA,
            0x14,
            0x01,
            0x00,
            0x42,
            0x16,
            0x01,
            0x92,
            0x07,
            0x01,
            0x00,
            0x00,
            0x67,
            0x00,
            0xDA,
            0x00,
            0x51,
            0x15,
            0x0D,
            0x0A,
        ),
    )
    payload = spi_read_command.parse(valid_resp)
    assert len(payload) == 7
    assert payload == array("B", (0x00, 0x67, 0x00, 0xDA, 0x00, 0x51, 0x15))

    valid_resp = array(
        "B",
        (
            0xAA,
            0x13,
            0x01,
            0x00,
            0x42,
            0x16,
            0x01,
            0x82,
            0x06,
            0x01,
            0x00,
            0x3F,
            0x00,
            0xFE,
            0xFF,
            0x17,
            0x00,
            0x0D,
            0x0A,
        ),
    )
    payload = spi_read_command.parse(valid_resp)
    assert len(payload) == 6
    assert payload == array("B", (0x3F, 0x00, 0xFE, 0xFF, 0x17, 0x00))


@pytest.mark.commands
def test_command_spi_write_assemble(spi_write_command: SPIWriteCmd) -> None:
    payload = spi_write_command.assemble(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5, start_register_address=0x0F, data_to_write=array("B", (0x03,))
    )

    expected_payload = array(
        "B",
        (
            0xAA,
            0x13,
            0x01,
            0x16,
            0x01,
            0x14,
            0x01,
            0x01,
            0x00,
            0x00,
            0x0F,
            0x00,
            0x01,
            0x01,
            0x00,
            0x00,
            0x03,
            0x0D,
            0x0A,
        ),
    )

    assert payload == expected_payload

    payload = spi_write_command.assemble(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1, start_register_address=0x7D, data_to_write=array("B", (0x04,))
    )

    expected_payload = array(
        "B",
        (
            0xAA,
            0x13,
            0x01,
            0x16,
            0x01,
            0x16,
            0x01,
            0x01,
            0x00,
            0x00,
            0x7D,
            0x00,
            0x01,
            0x01,
            0x00,
            0x00,
            0x04,
            0x0D,
            0x0A,
        ),
    )

    assert payload == expected_payload


@pytest.mark.commands
def test_command_spi_write_parse(spi_write_command: SPIWriteCmd) -> None:
    dummy_response = array("B", (0xD0, 0xDE))

    assert spi_write_command.parse(dummy_response) is None
