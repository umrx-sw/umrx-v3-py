import logging
import time
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
from umrx_app_v3.sensors.bmp390 import BMP390, BMP390Addr, BMP390NVMAddr

logger = logging.getLogger(__name__)


class BMP390ShuttleError(Exception): ...


class BMP390Shuttle:
    # 1-wire PROM
    SHUTTLE_ID = 0x173
    # Pins
    SDO = MultiIOPin.MINI_SHUTTLE_PIN_2_3
    CS = MultiIOPin.MINI_SHUTTLE_PIN_2_1
    INT1 = MultiIOPin.MINI_SHUTTLE_PIN_1_6
    # I2C addresses
    I2C_DEFAULT_ADDRESS = 0x76  # when SDO -> GND
    I2C_ALTERNATIVE_ADDRESS = 0x77  # when SDO -> VDDIO

    def __init__(self, **kw: Any) -> None:
        self.board: ApplicationBoard | None = kw["board"] if kw.get("board") else None
        self.sensor: BMP390 = BMP390()
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
            raise BMP390ShuttleError(error_message)

    def assign_sensor_callbacks(self) -> None:
        self.sensor.assign_callbacks(read_callback=self.read_register, write_callback=self.write_register)

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

    def read_register(self, reg_addr: int, bytes_to_read: int = 1) -> array[int] | int:
        if isinstance(reg_addr, (BMP390Addr | BMP390NVMAddr)):
            reg_addr = reg_addr.value
        if self.is_i2c_configured:
            values = self.board.read_i2c(self.I2C_DEFAULT_ADDRESS, reg_addr, bytes_to_read)
            if bytes_to_read == 1:
                return values[0]
            return values
        if self.is_spi_configured:
            if bytes_to_read == 1:
                return self.read_single_register_spi(reg_addr)
            return self.read_multiple_spi(reg_addr, bytes_to_read)

        error_message = "Configure I2C or SPI protocol prior to reading registers"
        raise BMP390ShuttleError(error_message)

    def read_single_register_spi(self, reg_addr: int) -> int:
        values = self.board.read_spi(self.CS, reg_addr, 2)
        return values[1]

    def read_multiple_spi(self, start_register_addr: int, bytes_to_read: int) -> array[int]:
        values = self.board.read_spi(self.CS, start_register_addr, bytes_to_read + 1)
        return values[1:]

    def write_register(self, reg_addr: int, value: int) -> None:
        if isinstance(reg_addr, (BMP390Addr | BMP390NVMAddr)):
            reg_addr = reg_addr.value
        if self.is_i2c_configured:
            return self.board.write_i2c(self.I2C_DEFAULT_ADDRESS, reg_addr, array("B", (value,)))
        if self.is_spi_configured:
            return self.board.write_spi(self.CS, reg_addr, array("B", (value,)))
        error_message = "Configure I2C or SPI protocol prior to reading registers"
        raise BMP390ShuttleError(error_message)

    def _configure_i2c_polling_streaming(
        self,
        sampling_time: int,
        sampling_unit: StreamingSamplingUnit,
    ) -> None:
        self.board.streaming_polling_set_i2c_channel(
            i2c_address=self.I2C_DEFAULT_ADDRESS,
            sampling_time=sampling_time,
            sampling_unit=sampling_unit,
            register_address=BMP390Addr.data_0.value,
            bytes_to_read=(3 + 3 + 2 + 3),
        )
        self.board.configure_streaming_polling(interface="i2c")
        self.is_polling_streaming_configured = True

    def _configure_spi_polling_streaming(
        self,
        sampling_time: int,
        sampling_unit: StreamingSamplingUnit,
    ) -> None:
        self.board.streaming_polling_set_spi_channel(
            cs_pin=self.CS,
            sampling_time=sampling_time,
            sampling_unit=sampling_unit,
            register_address=BMP390Addr.data_0.value,
            bytes_to_read=(1 + 3 + 3 + 2 + 3),
        )
        self.board.configure_streaming_polling(interface="spi")
        self.is_polling_streaming_configured = True

    def start_measurement(self) -> None:
        self.sensor.pwr_ctrl = (1 << 0) | (1 << 1) | (0b11 << 4)
        time.sleep(0.1)

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
        raise BMP390ShuttleError(error_message)

    def _configure_i2c_interrupt_streaming(self) -> None:
        self.board.streaming_interrupt_set_i2c_channel(
            interrupt_pin=self.INT1,
            i2c_address=self.I2C_DEFAULT_ADDRESS,
            register_address=BMP390Addr.data_0.value,
            bytes_to_read=(3 + 3 + 2 + 3),
        )
        self.board.configure_streaming_interrupt(interface="i2c")
        self.is_interrupt_streaming_configured = True

    def _configure_spi_interrupt_streaming(self) -> None:
        self.board.streaming_interrupt_set_spi_channel(
            interrupt_pin=self.INT1,
            cs_pin=self.CS,
            register_address=BMP390Addr.data_0.value,
            bytes_to_read=(1 + 3 + 3 + 2 + 3),
        )
        self.board.configure_streaming_interrupt(interface="spi")
        self.is_interrupt_streaming_configured = True

    def configure_interrupt_streaming(self) -> None:
        self.start_measurement()
        self.sensor.int_ctrl = (1 << 1) | (1 << 6)
        time.sleep(0.02)
        if self.is_i2c_configured:
            return self._configure_i2c_interrupt_streaming()
        if self.is_spi_configured:
            return self._configure_spi_interrupt_streaming()
        error_message = "Configure I2C or SPI protocol first"
        raise BMP390ShuttleError(error_message)

    def start_streaming(self) -> None:
        if self.is_polling_streaming_configured:
            return self.board.start_polling_streaming()
        if self.is_interrupt_streaming_configured:
            return self.board.start_interrupt_streaming()
        error_message = "Configure polling or interrupt streaming before streaming start"
        raise BMP390ShuttleError(error_message)

    def stop_streaming(self) -> None:
        self.board.stop_polling_streaming()
        time.sleep(0.15)
        self.board.stop_interrupt_streaming()
