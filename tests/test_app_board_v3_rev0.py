import logging

import pytest

from umrx_app_v3.mcu_board.app_board_v3_rev0 import ApplicationBoardV3Rev0
from umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from umrx_app_v3.mcu_board.comm.usb_comm import UsbCommunication

logger = logging.getLogger(__name__)


@pytest.mark.app_board
def test_app_board_v3_rev0_construction(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    assert isinstance(app_board_v3_rev0, ApplicationBoardV3Rev0), "Expecting instance of ApplicationBoard30"
    assert isinstance(app_board_v3_rev0.protocol, BstProtocol), "Expecting BST protocol object inside App Board 3.0"
    assert isinstance(app_board_v3_rev0.protocol.communication, UsbCommunication), "Expecting UsbCommunication"
