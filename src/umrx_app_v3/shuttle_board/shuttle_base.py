import logging
import time
from abc import abstractmethod
from array import array
from typing import Any, Self

from umrx_app_v3.mcu_board.app_board_v3_rev0 import ApplicationBoardV3Rev0
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_app_board import ApplicationBoard
from umrx_app_v3.mcu_board.bst_protocol_constants import (
    I2CMode,
    MultiIOPin,
    PinDirection,
    PinValue,
    SPIBus,
    StreamingSamplingUnit,
)
from umrx_app_v3.mcu_board.commands.spi import SPIConfigureCmd

logger = logging.getLogger(__name__)


class ShuttleBaseError(Exception): ...


class ShuttleBase:
    # 1-wire PROM
    SHUTTLE_ID = None
    # Pins
    SDO = MultiIOPin.MINI_SHUTTLE_PIN_2_3
    CS = MultiIOPin.MINI_SHUTTLE_PIN_2_1
    INT1 = MultiIOPin.MINI_SHUTTLE_PIN_1_6

    def __init__(self, **kw: Any) -> None:
        self.board: ApplicationBoard | None = kw["board"] if kw.get("board") else None
        self.sensor = None
        self.is_initialized: bool = False
        self.is_i2c_configured: bool = False
        self.is_spi_configured: bool = False
        self.is_polling_streaming_configured: bool = False
        self.is_interrupt_streaming_configured: bool = False

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
            raise ShuttleBaseError(error_message)

    @abstractmethod
    def assign_sensor_callbacks(self) -> None: ...

    def configure_i2c(self) -> None:
        self.board.set_pin_config(self.SDO, PinDirection.OUTPUT, PinValue.LOW)
        self.board.set_pin_config(self.CS, PinDirection.OUTPUT, PinValue.HIGH)
        self.board.set_vdd_vddio(3.3, 3.3)
        time.sleep(0.01)
        self.board.configure_i2c(I2CMode.FAST_MODE)
        self.assign_sensor_callbacks()
        self.is_i2c_configured = True
        self.is_spi_configured = False

    def configure_spi(self) -> None:
        self.board.set_pin_config(self.CS, PinDirection.OUTPUT, PinValue.HIGH)
        self.board.set_vdd_vddio(3.3, 3.3)
        time.sleep(0.2)
        if isinstance(self.board, ApplicationBoardV3Rev1):
            SPIConfigureCmd.set_bus(SPIBus.BUS_1)
        self.board.configure_spi()
        self.assign_sensor_callbacks()
        self.is_spi_configured = True
        self.is_i2c_configured = False


    @abstractmethod
    def read_register(self, reg_addr: int, bytes_to_read: int = 1) -> array[int] | int: ...

    @abstractmethod
    def write_register(self, reg_addr: int, value: int) -> None: ...

    def _configure_i2c_polling_streaming(
        self,
        sampling_time: int,
        sampling_unit: StreamingSamplingUnit,
    ) -> None: ...

    def _configure_spi_polling_streaming(
        self,
        sampling_time: int,
        sampling_unit: StreamingSamplingUnit,
    ) -> None: ...

    @abstractmethod
    def start_measurement(self) -> None: ...

    def configure_polling_streaming(
        self,
        sampling_time: int = 5,
        sampling_unit: StreamingSamplingUnit = StreamingSamplingUnit.MILLI_SECOND,
    ) -> None:
        self.start_measurement()
        if self.is_i2c_configured:
            return self._configure_i2c_polling_streaming(sampling_time, sampling_unit)
        if self.is_spi_configured:
            return self._configure_spi_polling_streaming(sampling_time, sampling_unit)
        error_message = "Configure I2C or SPI protocol first"
        raise ShuttleBaseError(error_message)

    def _configure_i2c_interrupt_streaming(self) -> None: ...

    def _configure_spi_interrupt_streaming(self) -> None: ...

    def configure_interrupt(self) -> None: ...

    def configure_interrupt_streaming(self) -> None:
        self.start_measurement()
        self.configure_interrupt()
        time.sleep(0.02)
        if self.is_i2c_configured:
            return self._configure_i2c_interrupt_streaming()
        if self.is_spi_configured:
            return self._configure_spi_interrupt_streaming()
        error_message = "Configure I2C or SPI protocol first"
        raise ShuttleBaseError(error_message)

    def start_streaming(self) -> None:
        if self.is_polling_streaming_configured:
            return self.board.start_polling_streaming()
        if self.is_interrupt_streaming_configured:
            return self.board.start_interrupt_streaming()
        error_message = "Configure polling or interrupt streaming before streaming start"
        raise ShuttleBaseError(error_message)

    def stop_streaming(self) -> None:
        self.board.stop_polling_streaming()
        time.sleep(0.15)
        self.board.stop_interrupt_streaming()
