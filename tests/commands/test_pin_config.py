from array import array

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, PinDirection, PinValue
from umrx_app_v3.mcu_board.commands.command import CommandError
from umrx_app_v3.mcu_board.commands.pin_config import GetPinConfigCmd, SetPinConfigCmd


@pytest.mark.commands
def test_command_set_pin(set_pin_config_command: SetPinConfigCmd) -> None:
    payload = set_pin_config_command.assemble(
        pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1, direction=PinDirection.OUTPUT, value=PinValue.HIGH
    )
    assert payload == array("B", (0xAA, 0x0C, 0x01, 0x15, 0x80, 0x16, 0x00, 0x01, 0x00, 0x01, 0x0D, 0x0A))

    payload = set_pin_config_command.assemble(
        pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5, direction=PinDirection.OUTPUT, value=PinValue.HIGH
    )

    assert payload == array("B", (0xAA, 0x0C, 0x01, 0x15, 0x80, 0x14, 0x00, 0x01, 0x00, 0x01, 0x0D, 0x0A))

    payload = set_pin_config_command.assemble(
        pin=MultiIOPin.MINI_SHUTTLE_PIN_2_6, direction=PinDirection.OUTPUT, value=PinValue.LOW
    )
    assert payload == array("B", (0xAA, 0x0C, 0x01, 0x15, 0x80, 0x15, 0x00, 0x01, 0x00, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_set_pin_parse(set_pin_config_command: SetPinConfigCmd) -> None:
    dummy_response = array("B", (0xBA, 0xBE))

    assert set_pin_config_command.parse(dummy_response) is None


@pytest.mark.commands
def test_command_get_pin_config(get_pin_config_command: GetPinConfigCmd) -> None:
    payload = get_pin_config_command.assemble(pin=MultiIOPin.MINI_SHUTTLE_PIN_2_6)
    assert payload == array("B", (0xAA, 0x08, 0x02, 0x15, 0x80, 0x15, 0x0D, 0x0A))

    payload = get_pin_config_command.assemble(pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1)
    assert payload == array("B", (0xAA, 0x08, 0x02, 0x15, 0x80, 0x16, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_get_pin_config_parse(get_pin_config_command: GetPinConfigCmd) -> None:
    response = array("B", (0xAA, 0x0E, 0x01, 0x00, 0x42, 0x15, 0x00, 0x15, 0x00, 0x01, 0x00, 0x00, 0x0D, 0x0A))
    direction, value = get_pin_config_command.parse(response)
    assert direction == PinDirection.OUTPUT
    assert value == PinValue.LOW

    response = array("B", (0xAA, 0x0E, 0x01, 0x00, 0x42, 0x15, 0x00, 0x16, 0x00, 0x01, 0x00, 0x00, 0x0D, 0x0A))
    direction, value = get_pin_config_command.parse(response)
    assert direction == PinDirection.OUTPUT
    assert value == PinValue.LOW


@pytest.mark.commands
def test_command_get_pin_config_parse_invalid(get_pin_config_command: GetPinConfigCmd) -> None:
    invalid_response = array("B", (0xAA, 0x0E, 0x01, 0x00, 0x42, 0x15, 0x00, 0x15, 0x00, 0x01, 0x00, 0x00))
    with pytest.raises(CommandError):
        get_pin_config_command.parse(invalid_response)
