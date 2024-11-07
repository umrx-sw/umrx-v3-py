import logging
import time

import pytest

from umrx_app_v3.mcu_board.app_board_v3_rev0 import ApplicationBoardV3Rev0
from umrx_app_v3.mcu_board.bst_app_board import BoardInfo
from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, PinDirection, PinValue

logger = logging.getLogger(__name__)


@pytest.mark.app_board
def test_app_board_v3_rev0_board_info(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.protocol.communication.connect()
    info = app_board_v3_rev0.board_info
    assert isinstance(info, BoardInfo), "Expecting BoardInfo instance"
    assert info.board_id == 0x05, "Wrong board ID"
    assert info.hardware_id == 0x10, "Wrong hardware ID"
    assert info.software_id == 0x09, "Wrong software ID"
    # assert info.shuttle_id == 0x66, "Wrong shuttle ID for BMI08x"
    assert info.shuttle_id == 0x141, "Wrong shuttle ID for BMI08x"


def test_app_board_v3_rev0_switch_app_mtp(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.protocol.communication.connect()
    app_board_v3_rev0.switch_usb_mtp()


def test_app_board_v3_rev0_switch_app_dfu(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.protocol.communication.connect()
    app_board_v3_rev0.switch_usb_dfu_bl()


def test_app_board_v3_rev0_read_bmi088_i2c_accel(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.initialize()
    app_board_v3_rev0.start_communication()
    info = app_board_v3_rev0.board_info
    assert info.shuttle_id == 0x66, "The integration test works only with BMI088"
    app_board_v3_rev0.set_vdd_vddio(3.3, 3.3)
    time.sleep(0.5)
    app_board_v3_rev0.configure_i2c()
    resp = app_board_v3_rev0.read_i2c(0x18, 0x0, 1)
    assert resp[0] == 0x1E, "Expect correct address for BMI088 accelerometer"


def test_gyro(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.initialize()
    app_board_v3_rev0.start_communication()
    info = app_board_v3_rev0.board_info
    assert info.shuttle_id == 0x66, "The integration test works only with BMI088"
    app_board_v3_rev0.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6, PinDirection.OUTPUT, PinValue.HIGH)
    app_board_v3_rev0.set_vdd_vddio(3.3, 3.3)
    time.sleep(0.5)
    app_board_v3_rev0.configure_i2c()
    resp = app_board_v3_rev0.read_i2c(0x68, 0x0, 1)
    assert resp[0] == 0x0F, "Expect correct address for BMI088 gyroscope"
