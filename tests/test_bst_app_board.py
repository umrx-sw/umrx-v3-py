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
        arg = array("B", [0xAA, 0x0C, 0x01, 0x14, 0x07, 0x08, 0x01, 0x0C, 0xE4, 0x01, 0x0D, 0x0A])
        mocked_send_receive.assert_called_with(arg)


@pytest.mark.app_board
def test_app_board_parse_board_info(bst_app_board_with_serial: ApplicationBoard) -> None:
    resp = array("B", [0xAA, 0x0F, 0x01, 0x00, 0x42, 0x1F, 0x01, 0x41, 0x00, 0x10, 0x00, 0x09, 0x05, 0x0D, 0x0A])
    board_info = bst_app_board_with_serial.parse_board_info(resp)

    assert board_info.hardware_id == 0x10

    assert board_info.software_id == 0x09

    assert board_info.board_id == 0x05

    assert board_info.shuttle_id == 0x141


@pytest.mark.app_board
def test_app_board_board_info(bst_app_board_with_serial: ApplicationBoard) -> None:
    resp = array("B", [0xAA, 0x0F, 0x01, 0x00, 0x42, 0x1F, 0x01, 0x41, 0x00, 0x10, 0x00, 0x09, 0x05, 0x0D, 0x0A])

    with patch.object(
        bst_app_board_with_serial.protocol.communication, "send_receive", return_value=resp
    ) as mocked_send_receive:
        info = bst_app_board_with_serial.board_info
        logger.info("info = %s", info)
        command_to_send = array("B", [0xAA, 0x06, 0x02, 0x1F, 0x0D, 0x0A])
        mocked_send_receive.assert_called_with(command_to_send)


@pytest.mark.app_board
def test_app_board_disable_timer(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol.communication, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.disable_timer()
        command_to_send = array("B", [0xAA, 0x07, 0x01, 0x29, 0x04, 0x0D, 0x0A])
        mocked_send_receive.assert_called_with(command_to_send)


@pytest.mark.app_board
def test_app_board_stop_polling_streaming(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol.communication, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.stop_polling_streaming()
        command_to_send = array("B", [0xAA, 0x06, 0x06, 0x00, 0x0D, 0x0A])
        mocked_send_receive.assert_called_with(command_to_send)


@pytest.mark.app_board
def test_app_board_stop_interrupt_streaming(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol.communication, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.stop_interrupt_streaming()
        command_to_send = array("B", [0xAA, 0x06, 0x0A, 0x00, 0x0D, 0x0A])
        mocked_send_receive.assert_called_with(command_to_send)


@pytest.mark.app_board
def test_app_board_switch_usb_mtp(bst_app_board_with_serial: ApplicationBoard) -> None:
    with (
        patch.object(bst_app_board_with_serial, "start_communication") as mocked_start_communication,
        patch.object(bst_app_board_with_serial, "switch_app") as mocked_switch_app,
    ):
        bst_app_board_with_serial.switch_usb_mtp()
        mocked_start_communication.assert_called_once()
        mocked_switch_app.assert_called_once()


@pytest.mark.app_board
def test_app_board_switch_usb_dfu_bl(bst_app_board_with_serial: ApplicationBoard) -> None:
    with (
        patch.object(bst_app_board_with_serial, "start_communication") as mocked_start_communication,
        patch.object(bst_app_board_with_serial, "switch_app") as mocked_switch_app,
    ):
        bst_app_board_with_serial.switch_usb_dfu_bl()
        mocked_start_communication.assert_called_once()
        mocked_switch_app.assert_called_once()
