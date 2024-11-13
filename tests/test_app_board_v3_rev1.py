import logging
from unittest.mock import patch

import pytest

from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from umrx_app_v3.mcu_board.comm.serial_comm import SerialCommunication

logger = logging.getLogger(__name__)


@pytest.mark.app_board
def test_app_board_v3_rev1_construction(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    assert isinstance(app_board_v3_rev1, ApplicationBoardV3Rev1), "Expecting instance of ApplicationBoard30"
    assert isinstance(app_board_v3_rev1.protocol, BstProtocol), "Expecting BST protocol object inside App Board 3.0"
    assert isinstance(app_board_v3_rev1.protocol.communication, SerialCommunication), "Expecting SerialCommunication"


@pytest.mark.app_board
def test_app_board_v3_rev1_switch_usb_dfu_bl(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    with patch.object(app_board_v3_rev1.usb_comm, "send_control_transfer") as mocked_ctrl_transfer:
        app_board_v3_rev1.switch_usb_dfu_bl()
        mocked_ctrl_transfer.assert_called_once()


@pytest.mark.app_board
def test_app_board_v3_rev1_switch_mtp(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    with patch.object(app_board_v3_rev1.usb_comm, "send_control_transfer") as mocked_ctrl_transfer:
        app_board_v3_rev1.switch_usb_mtp()
        mocked_ctrl_transfer.assert_called_once()


@pytest.mark.app_board
def test_app_board_v3_rev1_initialize_usb(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    with patch.object(app_board_v3_rev1.usb_comm, "initialize") as mocked_usb_initialize:
        assert not app_board_v3_rev1.usb_comm.is_initialized

        app_board_v3_rev1.initialize_usb()

        mocked_usb_initialize.assert_called_once()


@pytest.mark.app_board
def test_app_board_v3_rev1_do_not_double_initialize_usb(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    with patch.object(app_board_v3_rev1.usb_comm, "initialize") as mocked_usb_initialize:
        app_board_v3_rev1.usb_comm.is_initialized = True

        app_board_v3_rev1.initialize_usb()

        mocked_usb_initialize.assert_not_called()

        app_board_v3_rev1.usb_comm.is_initialized = False


@pytest.mark.app_board
def test_app_board_v3_rev1_initialize(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    with patch.object(app_board_v3_rev1.protocol.communication, "initialize") as mocked_protocol_initialize:
        assert not app_board_v3_rev1.protocol.communication.is_initialized

        app_board_v3_rev1.initialize()

        mocked_protocol_initialize.assert_called_once()


@pytest.mark.app_board
def test_app_board_v3_rev1_receive_streaming_multiple(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    example_payload = (
        b"\xaa\x0f\x01\x00\x87\x00\x00\x00\x00\x00\x00\x00\x01\r\n\xaa\x0f\x01\x00\x87N\x00v\x00"
        b"\x8e\x05\x00\x02\r\n\xaa\x0f\x01\x00\x87\x00\x00\x00\x00\x00\x00\x00\x01\r\n"
    )

    with patch.object(
        app_board_v3_rev1.protocol.communication, "_receive", return_value=example_payload
    ) as mocked_protocol_initialize:
        num_messages = 0
        for message in app_board_v3_rev1.receive_streaming_multiple():
            logger.info(f"{message=}")
            num_messages += 1

        assert num_messages == 3
        mocked_protocol_initialize.assert_called_once()
