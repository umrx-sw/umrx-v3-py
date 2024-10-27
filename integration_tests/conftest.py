import logging
import sys

import pytest

from umrx_app_v3.mcu_board.app_board_v3_rev0 import ApplicationBoardV3Rev0
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from umrx_app_v3.mcu_board.comm.serial_comm import SerialCommunication
from umrx_app_v3.mcu_board.comm.usb_comm import UsbCommunication
from umrx_app_v3.shuttle_board.bmi088 import BMI088

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s][%(levelname)-8s][%(name)s]: %(message)s"
    )
)

# get root logger
logger = logging.getLogger()
logger.handlers = []
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


@pytest.fixture(scope="session", autouse=True)
def usb_comm() -> UsbCommunication:
    return UsbCommunication()


@pytest.fixture(scope="session", autouse=True)
def serial_comm() -> SerialCommunication:
    return SerialCommunication()


@pytest.fixture(scope="session", autouse=True)
def bst_protocol_usb(usb_comm: UsbCommunication) -> BstProtocol:
    return BstProtocol(comm="usb", usb=usb_comm)


@pytest.fixture(scope="session", autouse=True)
def bst_protocol_serial(serial_comm: SerialCommunication) -> BstProtocol:
    return BstProtocol(comm="serial", serial=serial_comm)


@pytest.fixture(scope="session", autouse=True)
def app_board_v3_rev0(bst_protocol_usb: BstProtocol) -> ApplicationBoardV3Rev0:
    return ApplicationBoardV3Rev0(protocol=bst_protocol_usb)


@pytest.fixture(scope="session", autouse=True)
def app_board_v3_rev1(bst_protocol_serial: BstProtocol) -> ApplicationBoardV3Rev1:
    return ApplicationBoardV3Rev1(protocol=bst_protocol_serial)


@pytest.fixture(scope="session", autouse=True)
def bmi088(app_board_v3_rev0: ApplicationBoardV3Rev0) -> BMI088:
    return BMI088(board=app_board_v3_rev0)
