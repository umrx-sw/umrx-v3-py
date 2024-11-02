import logging
from array import array
from unittest.mock import patch

import pytest

from umrx_app_v3.mcu_board.bst_app_board import ApplicationBoard
from umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from umrx_app_v3.mcu_board.comm.serial_comm import SerialCommunication

logger = logging.getLogger(__name__)


@pytest.mark.app_board
def test_app_board_construction(bst_app_board_with_serial: ApplicationBoard) -> None:
    assert isinstance(bst_app_board_with_serial, ApplicationBoard), "Expecting instance of ApplicationBoard30"
    assert isinstance(bst_app_board_with_serial.protocol, BstProtocol), "Expect BST protocol object inside App Board"
    assert isinstance(bst_app_board_with_serial.protocol.communication, SerialCommunication), "Expecting Serial"


@pytest.mark.app_board
def test_app_board_voltage_to_payload(bst_app_board_with_serial: ApplicationBoard) -> None:
    payload = bst_app_board_with_serial.voltage_to_payload(1.8)
    assert payload == (0x07, 0x08)

    payload = bst_app_board_with_serial.voltage_to_payload(3.3)
    assert payload == (0x0C, 0xE4)


@pytest.mark.app_board
def test_app_board_vdd_vddio(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol.communication, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.set_vdd_vddio(1.8, 3.3)
        arg = array('B', [0xAA, 0x0C, 0x01, 0x14, 0x07, 0x08, 0x01, 0x0C, 0xE4, 0x01, 0x0D, 0x0A])
        mocked_send_receive.assert_called_with(arg)
