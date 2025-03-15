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
    StreamingSamplingUnit,
)
from umrx_app_v3.sensors.bmm350 import BMM350, BMM350Addr

logger = logging.getLogger(__name__)


class BMM350ShuttleError(Exception): ...


class BMM350Shuttle:
    # 1-wire PROM
    SHUTTLE_ID = 0x27
    # Pins
    INT = MultiIOPin.MINI_SHUTTLE_PIN_1_6
    ADSEL = MultiIOPin.MINI_SHUTTLE_PIN_1_4
    # I2C addresses
    I2C_DEFAULT_ADDRESS = 0x14
    I2C_ALTERNATIVE_ADDRESS = 0x15

    def __init__(self, **kw: Any) -> None:
        self.board: ApplicationBoard | None = kw["board"] if kw.get("board") else None
        self.sensor: BMM350 = BMM350()
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
            raise BMM350ShuttleError(error_message)

    def assign_sensor_callbacks(self) -> None:
        self.sensor.assign_callbacks(read_callback=self.read_register, write_callback=self.write_register)

    def configure_i2c(self) -> None:
        self.board.set_vdd_vddio(0.0, 0.0)
        time.sleep(0.1)
        self.board.set_pin_config(self.ADSEL, PinDirection.OUTPUT, PinValue.LOW)
        self.board.set_vdd_vddio(2.7, 2.7)
        time.sleep(0.01)
        self.board.configure_i2c(I2CMode.FAST_MODE)
        self.assign_sensor_callbacks()
        self.is_i2c_configured = True
        self.is_spi_configured = False

    def read_register(self, reg_addr: int, bytes_to_read: int = 1) -> array[int] | int:
        if isinstance(reg_addr, BMM350Addr):
            reg_addr = reg_addr.value
        if self.is_i2c_configured:
            values = self.board.read_i2c(self.I2C_DEFAULT_ADDRESS, reg_addr, bytes_to_read + 2)
            if bytes_to_read == 1:
                return values[2]
            return values[2:]
        error_message = "Configure I2C protocol prior to reading registers"
        raise BMM350ShuttleError(error_message)

    def write_register(self, reg_addr: int, value: int) -> None:
        if isinstance(reg_addr, BMM350Addr):
            reg_addr = reg_addr.value
        if self.is_i2c_configured:
            return self.board.write_i2c(self.I2C_DEFAULT_ADDRESS, reg_addr, array("B", (value,)))
        error_message = "Configure I2C protocol prior to reading registers"
        raise BMM350ShuttleError(error_message)

    def _configure_i2c_polling_streaming(
        self,
        sampling_time: int,
        sampling_unit: StreamingSamplingUnit,
    ) -> None:
        self.board.streaming_polling_set_i2c_channel(
            i2c_address=self.I2C_DEFAULT_ADDRESS,
            sampling_time=sampling_time,
            sampling_unit=sampling_unit,
            register_address=BMM350Addr.mag_x_xlsb.value,
            bytes_to_read=(2 + 9 + 3 + 3),
        )
        self.board.configure_streaming_polling(interface="i2c")
        self.is_polling_streaming_configured = True

    def close_otp(self) -> None:
        self.sensor.otp_cmd_reg = 0x80

    def start_measurement(self) -> None:
        self.sensor.pmu_cmd_axis_en = (1 << 2) | (1 << 1) | (1 << 0)
        self.sensor.pmu_cmd_aggr_set = 0x14
        self.sensor.pmu_cmd = 0x1

    def configure_polling_streaming(
        self,
        sampling_time: int = 1,
        sampling_unit: StreamingSamplingUnit = StreamingSamplingUnit.MILLI_SECOND,
    ) -> None:
        self.start_measurement()
        if self.is_i2c_configured:
            return self._configure_i2c_polling_streaming(sampling_time, sampling_unit)
        error_message = "Configure I2C protocol first"
        raise BMM350ShuttleError(error_message)

    def _configure_i2c_interrupt_streaming(self) -> None:
        self.board.streaming_interrupt_set_i2c_channel(
            interrupt_pin=self.INT,
            i2c_address=self.I2C_DEFAULT_ADDRESS,
            register_address=BMM350Addr.mag_x_xlsb.value,
            bytes_to_read=(2 + 9 + 3 + 3),
        )
        self.board.configure_streaming_interrupt(interface="i2c")
        self.is_interrupt_streaming_configured = True

    def configure_interrupt_streaming(self) -> None:
        self.start_measurement()
        self.sensor.int_ctrl = (1 << 7) | (1 << 3) | (1 << 2) | (1 << 1)
        time.sleep(0.02)
        if self.is_i2c_configured:
            return self._configure_i2c_interrupt_streaming()
        error_message = "Configure I2C protocol first"
        raise BMM350ShuttleError(error_message)

    def start_streaming(self) -> None:
        if self.is_polling_streaming_configured:
            return self.board.start_polling_streaming()
        if self.is_interrupt_streaming_configured:
            return self.board.start_interrupt_streaming()
        error_message = "Configure polling or interrupt streaming before streaming start"
        raise BMM350ShuttleError(error_message)

    def stop_streaming(self) -> None:
        self.board.stop_polling_streaming()
        time.sleep(0.15)
        self.board.stop_interrupt_streaming()
