import logging
import sys

import pytest

from umrx_app_v3.mcu_board.app_board_v3_rev0 import ApplicationBoardV3Rev0
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_app_board import ApplicationBoard
from umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from umrx_app_v3.mcu_board.comm.serial_comm import SerialCommunication
from umrx_app_v3.mcu_board.comm.usb_comm import UsbCommunication
from umrx_app_v3.mcu_board.commands.app_switch import AppSwitchCmd
from umrx_app_v3.mcu_board.commands.board_info import BoardInfoCmd
from umrx_app_v3.mcu_board.commands.i2c import I2CConfigureCmd, I2CReadCmd, I2CWriteCmd
from umrx_app_v3.mcu_board.commands.pin_config import GetPinConfigCmd, SetPinConfigCmd
from umrx_app_v3.mcu_board.commands.set_vdd_vddio import SetVddVddioCmd
from umrx_app_v3.mcu_board.commands.spi import SPIConfigureCmd, SPIReadCmd, SPIWriteCmd
from umrx_app_v3.mcu_board.commands.streaming_interrupt import StreamingInterruptCmd
from umrx_app_v3.mcu_board.commands.streaming_polling import (
    StreamingPollingCmd,
)
from umrx_app_v3.mcu_board.commands.timer import TimerCmd
from umrx_app_v3.shuttle_board.bmi088.bmi088_shuttle import BMI088Shuttle

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)-8s][%(name)s]: %(message)s"))

# get root logger
logger = logging.getLogger()
logger.handlers = []
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


@pytest.fixture(scope="session", autouse=True)
def app_switch_cmd() -> AppSwitchCmd:
    return AppSwitchCmd()


@pytest.fixture(scope="session", autouse=True)
def board_info_cmd() -> BoardInfoCmd:
    return BoardInfoCmd()


@pytest.fixture(scope="session", autouse=True)
def set_vdd_vddio_command() -> SetVddVddioCmd:
    return SetVddVddioCmd()


@pytest.fixture(scope="session", autouse=True)
def set_pin_config_command() -> SetPinConfigCmd:
    return SetPinConfigCmd()


@pytest.fixture(scope="session", autouse=True)
def get_pin_config_command() -> GetPinConfigCmd:
    return GetPinConfigCmd()


@pytest.fixture(scope="session", autouse=True)
def i2c_configure_command() -> I2CConfigureCmd:
    return I2CConfigureCmd()


@pytest.fixture(scope="session", autouse=True)
def i2c_read_command() -> I2CReadCmd:
    return I2CReadCmd()


@pytest.fixture(scope="session", autouse=True)
def i2c_write_command() -> I2CWriteCmd:
    return I2CWriteCmd()


@pytest.fixture(scope="session", autouse=True)
def spi_configure_command() -> SPIConfigureCmd:
    return SPIConfigureCmd()


@pytest.fixture(scope="session", autouse=True)
def spi_read_command() -> SPIReadCmd:
    return SPIReadCmd()


@pytest.fixture(scope="session", autouse=True)
def spi_write_command() -> SPIWriteCmd:
    return SPIWriteCmd()


@pytest.fixture(scope="session", autouse=True)
def streaming_interrupt_command() -> StreamingInterruptCmd:
    return StreamingInterruptCmd()


@pytest.fixture
def streaming_polling_command() -> StreamingPollingCmd:
    return StreamingPollingCmd()


@pytest.fixture
def timer_command() -> TimerCmd:
    return TimerCmd()


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
def bst_app_board_with_serial(bst_protocol_serial: SerialCommunication) -> ApplicationBoard:
    return ApplicationBoard(protocol=bst_protocol_serial)


@pytest.fixture(scope="session", autouse=True)
def bst_app_board_with_usb(bst_protocol_usb: UsbCommunication) -> ApplicationBoard:
    return ApplicationBoard(protocol=bst_protocol_usb)


@pytest.fixture(scope="session", autouse=True)
def app_board_v3_rev0(bst_protocol_usb: BstProtocol) -> ApplicationBoardV3Rev0:
    return ApplicationBoardV3Rev0(protocol=bst_protocol_usb)


@pytest.fixture(scope="session", autouse=True)
def app_board_v3_rev1(bst_protocol_serial: BstProtocol) -> ApplicationBoardV3Rev1:
    return ApplicationBoardV3Rev1(protocol=bst_protocol_serial)


@pytest.fixture(scope="session", autouse=True)
def bmi088_shuttle(app_board_v3_rev0: ApplicationBoardV3Rev0) -> BMI088Shuttle:
    return BMI088Shuttle(board=app_board_v3_rev0)
