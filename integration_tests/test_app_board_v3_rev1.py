import logging

import pytest

from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_app_board import BoardInfo

logger = logging.getLogger(__name__)


@pytest.mark.app_board
def test_app_board_v3_rev0_board_info(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    app_board_v3_rev1.protocol.communication.connect()
    app_board_v3_rev1.stop_polling_streaming()
    info = app_board_v3_rev1.board_info
    assert isinstance(info, BoardInfo), "Expecting BoardInfo instance"
    assert info.board_id == 0x09, "Wrong board ID"
    assert info.hardware_id == 0x11, "Wrong hardware ID"
    assert info.software_id == 0x171, "Wrong software ID"
    assert info.shuttle_id == 0x66, "Wrong shuttle ID for BMI08x"


def test_app_board_v3_rev1_switch_app_mtp(app_board_v3_rev1: ApplicationBoardV3Rev1):
    app_board_v3_rev1.protocol.communication.connect()
    app_board_v3_rev1.switch_usb_mtp()
