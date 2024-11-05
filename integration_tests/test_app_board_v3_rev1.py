import logging
import time

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


@pytest.mark.app_board
def test_app_board_v3_rev1_switch_app_mtp(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    app_board_v3_rev1.initialize_usb()
    app_board_v3_rev1.switch_usb_mtp()


@pytest.mark.app_board
def test_app_board_v3_rev1_switch_usb_dfu_bl(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    app_board_v3_rev1.initialize_usb()
    app_board_v3_rev1.switch_usb_dfu_bl()


@pytest.mark.app_board
def test_app_board_v3_rev1_read_bmi088_i2c_gyro(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    app_board_v3_rev1.initialize()
    app_board_v3_rev1.start_communication()
    info = app_board_v3_rev1.board_info
    assert info.shuttle_id == 0x66, "The integration test works only with BMI088"
    app_board_v3_rev1.set_vdd_vddio(3.3, 3.3)
    time.sleep(0.5)
    app_board_v3_rev1.configure_i2c()
    resp = app_board_v3_rev1.read_i2c(0x68, 0x0, 1)
    assert resp[0] == 0x0F, "Expect correct address for BMI088 gyroscope"


@pytest.mark.app_board
def test_app_board_v3_rev1_read_bmi088_i2c_accel(app_board_v3_rev1: ApplicationBoardV3Rev1) -> None:
    app_board_v3_rev1.initialize()
    app_board_v3_rev1.start_communication()
    info = app_board_v3_rev1.board_info
    assert info.shuttle_id == 0x66, "The integration test works only with BMI088"
    app_board_v3_rev1.set_vdd_vddio(3.3, 3.3)
    time.sleep(0.5)
    app_board_v3_rev1.configure_i2c()
    resp = app_board_v3_rev1.read_i2c(0x18, 0x0, 1)
    assert resp[0] == 0x1E, "Expect correct address for BMI088 accelerometer"
