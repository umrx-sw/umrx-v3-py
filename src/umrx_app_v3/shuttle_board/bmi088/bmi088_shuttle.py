import logging
from array import array
from typing import Any, Self

from umrx_app_v3.mcu_board.app_board_v3_rev0 import ApplicationBoardV3Rev0
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_app_board import ApplicationBoard
from umrx_app_v3.sensors.bmi088 import BMI088
from umrx_app_v3.shuttle_board.bmi088.accel_streaming_packet import BMI088AccelPacket
from umrx_app_v3.shuttle_board.bmi088.gyro_streaming_packet import BMI088GyroPacket

logger = logging.getLogger(__name__)


class BMI088ShuttleError(Exception): ...


class BMI088Shuttle:
    SHUTTLE_ID = 0x66

    def __init__(self, **kw: Any) -> None:
        self.board: ApplicationBoard | None = kw["board"] if kw.get("board") else None
        self.sensor: BMI088 = BMI088()
        self.is_initialized: bool = False

    def attach_to(self, board: ApplicationBoard) -> None:
        self.board = board

    @classmethod
    def on_hardware_v3_rev0(cls) -> Self:
        return cls(board=ApplicationBoardV3Rev0())

    @classmethod
    def on_hardware_v3_rev1(cls) -> Self:
        return cls(board=ApplicationBoardV3Rev1())

    def initialize(self) -> None:
        self.board.initialize()
        self.board.start_communication()
        self.is_initialized = True

    def check_connected_hw(self) -> None:
        board_info = self.board.board_info
        if board_info.shuttle_id != self.SHUTTLE_ID:
            error_message = f"Expect shuttle_id={self.SHUTTLE_ID} got {board_info.shuttle_id}"
            raise BMI088ShuttleError(error_message)

    def configure_i2c(self) -> None:
        raise NotImplementedError

    def configure_spi(self) -> None:
        raise NotImplementedError

    def read_accel_register(self, reg_addr: int) -> None:
        raise NotImplementedError

    def write_accel_register(self, reg_addr: int, value: int) -> None:
        raise NotImplementedError

    def read_gyro_register(self, reg_addr: int) -> None:
        raise NotImplementedError

    def write_gyro_register(self, reg_addr: int, value: int) -> None:
        raise NotImplementedError

    def configure_polling_streaming(self) -> None:
        raise NotImplementedError

    def configure_interrupt_streaming(self) -> None:
        self.sensor.gyro_lpm1 = 0x23
        raise NotImplementedError

    def start_streaming(self) -> None:
        raise NotImplementedError

    def stop_streaming(self) -> None:
        raise NotImplementedError

    def decode_gyro_streaming(self, packet: array[int]) -> BMI088GyroPacket:
        raise NotImplementedError

    def decode_accel_streaming(self, packet: array[int]) -> BMI088AccelPacket:
        raise NotImplementedError
