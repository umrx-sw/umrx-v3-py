from array import array

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, PinDirection, PinValue
from umrx_app_v3.mcu_board.commands.pin_config import SetPinConfigCmd


@pytest.mark.commands
def test_app_board_set_pin(set_pin_config_command: SetPinConfigCmd) -> None:
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
def test_app_board_set_pin_parse(set_pin_config_command: SetPinConfigCmd) -> None:
    dummy_response = array("B", (0xBA, 0xBE))

    assert set_pin_config_command.parse(dummy_response) is None
