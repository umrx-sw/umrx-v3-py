import pytest
from umrx_app_v3.mcu_board.commands.set_vdd_vddio import SetVddVddioCmd

@pytest.mark.app_board
def test_app_board_voltage_to_payload(set_vdd_vddio_command: SetVddVddioCmd) -> None:
    payload = set_vdd_vddio_command.voltage_to_payload(1.8)
    assert payload == (0x07, 0x08)

    payload = set_vdd_vddio_command.voltage_to_payload(3.3)
    assert payload == (0x0C, 0xE4)
