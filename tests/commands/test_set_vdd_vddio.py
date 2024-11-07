from array import array

import pytest

from umrx_app_v3.mcu_board.commands.set_vdd_vddio import SetVddVddioCmd


@pytest.mark.commands
def test_app_board_voltage_to_payload(set_vdd_vddio_command: SetVddVddioCmd) -> None:
    payload = set_vdd_vddio_command.voltage_to_payload(1.8)
    assert payload == (0x07, 0x08)

    payload = set_vdd_vddio_command.voltage_to_payload(3.3)
    assert payload == (0x0C, 0xE4)


@pytest.mark.commands
def test_app_board_parse(set_vdd_vddio_command: SetVddVddioCmd) -> None:
    dummy_message = array("B", (0xCA, 0xFE))

    assert set_vdd_vddio_command.parse(dummy_message) is None
