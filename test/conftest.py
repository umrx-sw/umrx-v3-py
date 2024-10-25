import logging
import os
import pathlib
import sys
import pytest

from umrx_app_v3.mcu_board.usb_comm import UsbCommunication
from src.umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from src.umrx_app_v3.mcu_board.app_board_30 import ApplicationBoard30

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


@pytest.fixture(scope='session', autouse=True)
def usb_comm() -> UsbCommunication:
    return UsbCommunication()


@pytest.fixture(scope='session', autouse=True)
def bst_protocol(usb_comm: UsbCommunication) -> BstProtocol:
    return BstProtocol(usb=usb_comm)


@pytest.fixture(scope='session', autouse=True)
def app_board_30(bst_protocol: BstProtocol) -> ApplicationBoard30:
    return ApplicationBoard30(protocol=bst_protocol)


@pytest.fixture(scope='session', autouse=True)
def bmi088(app_board_30: ApplicationBoard30) -> BMI088:
    return BMI088(board=app_board_30)

