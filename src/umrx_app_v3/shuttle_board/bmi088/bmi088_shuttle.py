import logging
import struct
import time
from array import array
from typing import Any, Self

from umrx_app_v3.mcu_board.app_board_v3_rev0 import ApplicationBoardV3Rev0
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_app_board import ApplicationBoard
from umrx_app_v3.mcu_board.bst_protocol_constants import (
    MultiIOPin,
    PinDirection,
    PinValue,
    SPIBus,
    StreamingSamplingUnit,
)
from umrx_app_v3.mcu_board.commands.spi import SPIConfigureCmd
from umrx_app_v3.sensors.bmi088 import BMI088, BMI088AccelAddr, BMI088GyroAddr
from umrx_app_v3.shuttle_board.bmi088.accel_streaming_packet import BMI088AccelPacket
from umrx_app_v3.shuttle_board.bmi088.gyro_streaming_packet import BMI088GyroPacket

logger = logging.getLogger(__name__)


class BMI088ShuttleError(Exception): ...


class BMI088Shuttle:
    # 1-wire PROM
    SHUTTLE_ID = 0x66
    # Pins
    SDO = MultiIOPin.MINI_SHUTTLE_PIN_2_3
    CSB1 = MultiIOPin.MINI_SHUTTLE_PIN_2_1
    CSB2 = MultiIOPin.MINI_SHUTTLE_PIN_2_5
    PS = MultiIOPin.MINI_SHUTTLE_PIN_2_6
    INT1 = MultiIOPin.MINI_SHUTTLE_PIN_1_6
    INT3 = MultiIOPin.MINI_SHUTTLE_PIN_1_7
    # I2C addresses
    GYRO_I2C_DEFAULT_ADDRESS = 0x68
    ACCEL_I2C_DEFAULT_ADDRESS = 0x18

    def __init__(self, **kw: Any) -> None:
        self.board: ApplicationBoard | None = kw["board"] if kw.get("board") else None
        self.sensor: BMI088 = BMI088()
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
            raise BMI088ShuttleError(error_message)

    def assign_sensor_callbacks(self) -> None:
        self.sensor.assign_gyro_callbacks(
            read_callback=self.read_gyro_register, write_callback=self.write_gyro_register
        )
        self.sensor.assign_accel_callbacks(
            read_callback=self.read_accel_register, write_callback=self.write_accel_register
        )

    def configure_i2c(self) -> None:
        self.board.set_pin_config(self.PS, PinDirection.OUTPUT, PinValue.HIGH)
        self.board.set_vdd_vddio(3.3, 3.3)
        time.sleep(0.01)
        self.board.configure_i2c()
        self.assign_sensor_callbacks()
        self.is_i2c_configured = True
        self.is_spi_configured = False

    def configure_spi(self) -> None:
        self.board.set_pin_config(self.CSB1, PinDirection.OUTPUT, PinValue.HIGH)
        self.board.set_pin_config(self.CSB2, PinDirection.OUTPUT, PinValue.HIGH)
        self.board.set_pin_config(self.PS, PinDirection.OUTPUT, PinValue.LOW)
        time.sleep(0.01)
        self.board.set_vdd_vddio(3.3, 3.3)
        time.sleep(0.2)
        if isinstance(self.board, ApplicationBoardV3Rev1):
            SPIConfigureCmd.set_bus(SPIBus.BUS_1)
        self.board.configure_spi()
        self.assign_sensor_callbacks()
        self.is_spi_configured = True
        self.is_i2c_configured = False

    def read_accel_register(self, reg_addr: int, bytes_to_read: int = 1) -> array[int] | int:
        if isinstance(reg_addr, BMI088AccelAddr):
            reg_addr = reg_addr.value
        if self.is_i2c_configured:
            values = self.board.read_i2c(self.ACCEL_I2C_DEFAULT_ADDRESS, reg_addr, bytes_to_read)
            if bytes_to_read == 1:
                return values[0]
            return values
        if self.is_spi_configured:
            if bytes_to_read == 1:
                _ = self.board.read_spi(self.CSB1, reg_addr, 1)
            values = self.board.read_spi(self.CSB1, reg_addr, bytes_to_read + 1)
            if bytes_to_read == 1:
                return values[0]
            return values[1:]
        error_message = "Configure I2C or SPI protocol prior to reading registers"
        raise BMI088ShuttleError(error_message)

    def write_accel_register(self, reg_addr: int, value: int) -> None:
        if isinstance(reg_addr, BMI088AccelAddr):
            reg_addr = reg_addr.value
        if self.is_i2c_configured:
            return self.board.write_i2c(self.ACCEL_I2C_DEFAULT_ADDRESS, reg_addr, array("B", (value,)))
        if self.is_spi_configured:
            return self.board.write_spi(self.CSB1, reg_addr, array("B", (value,)))
        error_message = "Configure I2C or SPI protocol prior to reading registers"
        raise BMI088ShuttleError(error_message)

    def read_gyro_register(self, reg_addr: int, bytes_to_read: int = 1) -> array[int] | int:
        if isinstance(reg_addr, BMI088GyroAddr):
            reg_addr = reg_addr.value
        if self.is_i2c_configured:
            values = self.board.read_i2c(self.GYRO_I2C_DEFAULT_ADDRESS, reg_addr, bytes_to_read)
            if bytes_to_read == 1:
                return values[0]
            return values
        if self.is_spi_configured:
            values = self.board.read_spi(self.CSB2, reg_addr, bytes_to_read)
            if bytes_to_read == 1:
                return values[0]
            return values
        error_message = "Configure I2C or SPI protocol prior to reading registers"
        raise BMI088ShuttleError(error_message)

    def write_gyro_register(self, reg_addr: int, value: int) -> None:
        if isinstance(reg_addr, BMI088GyroAddr):
            reg_addr = reg_addr.value
        if self.is_i2c_configured:
            return self.board.write_i2c(self.GYRO_I2C_DEFAULT_ADDRESS, reg_addr, array("B", (value,)))
        if self.is_spi_configured:
            return self.board.write_spi(self.CSB2, reg_addr, array("B", (value,)))
        error_message = "Configure I2C or SPI protocol prior to reading registers"
        raise BMI088ShuttleError(error_message)

    def _configure_i2c_polling_streaming(
        self,
        accel_sampling_time: int,
        accel_sampling_unit: StreamingSamplingUnit,
        gyro_sampling_time: int,
        gyro_sampling_unit: StreamingSamplingUnit,
    ) -> None:
        self.board.streaming_polling_set_i2c_channel(
            i2c_address=0x18,
            sampling_time=accel_sampling_time,
            sampling_unit=accel_sampling_unit,
            register_address=0x12,
            bytes_to_read=6,
        )
        self.board.streaming_polling_set_i2c_channel(
            i2c_address=0x68,
            sampling_time=gyro_sampling_time,
            sampling_unit=gyro_sampling_unit,
            register_address=0x02,
            bytes_to_read=6,
        )
        self.board.configure_streaming_polling(interface="i2c")
        self.is_polling_streaming_configured = True

    def _configure_spi_polling_streaming(
        self,
        accel_sampling_time: int,
        accel_sampling_unit: StreamingSamplingUnit,
        gyro_sampling_time: int,
        gyro_sampling_unit: StreamingSamplingUnit,
    ) -> None:
        self.board.streaming_polling_set_spi_channel(
            cs_pin=self.CSB1,
            sampling_time=accel_sampling_time,
            sampling_unit=accel_sampling_unit,
            register_address=0x12,
            bytes_to_read=7,
        )
        self.board.streaming_polling_set_spi_channel(
            cs_pin=self.CSB2,
            sampling_time=gyro_sampling_time,
            sampling_unit=gyro_sampling_unit,
            register_address=0x02,
            bytes_to_read=6,
        )
        self.board.configure_streaming_polling(interface="spi")
        self.is_polling_streaming_configured = True

    def switch_on_accel(self) -> None:
        self.sensor.acc_pwr_conf = 0x00
        self.sensor.acc_pwr_ctrl = 0x04

    def configure_polling_streaming(
        self,
        accel_sampling_time: int = 625,
        accel_sampling_unit: StreamingSamplingUnit = StreamingSamplingUnit.MICRO_SECOND,
        gyro_sampling_time: int = 500,
        gyro_sampling_unit: StreamingSamplingUnit = StreamingSamplingUnit.MICRO_SECOND,
    ) -> None:
        self.switch_on_accel()
        if self.is_i2c_configured:
            return self._configure_i2c_polling_streaming(
                accel_sampling_time, accel_sampling_unit, gyro_sampling_time, gyro_sampling_unit
            )
        if self.is_spi_configured:
            return self._configure_spi_polling_streaming(
                accel_sampling_time, accel_sampling_unit, gyro_sampling_time, gyro_sampling_unit
            )
        error_message = "Configure I2C or SPI protocol first"
        raise BMI088ShuttleError(error_message)

    def _configure_i2c_interrupt_streaming(self) -> None:
        self.board.streaming_interrupt_set_i2c_channel(
            interrupt_pin=self.INT1,
            i2c_address=0x18,
            register_address=0x12,
            bytes_to_read=6,
        )
        self.board.streaming_interrupt_set_i2c_channel(
            interrupt_pin=self.INT3,
            i2c_address=0x68,
            register_address=0x02,
            bytes_to_read=6,
        )
        self.board.configure_streaming_interrupt(interface="i2c")
        self.is_interrupt_streaming_configured = True

    def _configure_spi_interrupt_streaming(self) -> None:
        self.board.streaming_interrupt_set_spi_channel(
            interrupt_pin=self.INT1,
            cs_pin=self.CSB1,
            register_address=0x12,
            bytes_to_read=7,
        )
        self.board.streaming_interrupt_set_spi_channel(
            interrupt_pin=self.INT3,
            cs_pin=self.CSB2,
            register_address=0x02,
            bytes_to_read=6,
        )
        self.board.configure_streaming_interrupt(interface="spi")
        self.is_interrupt_streaming_configured = True

    def configure_interrupt_streaming(self) -> None:
        self.switch_on_accel()
        self.sensor.acc_int1_io_ctrl = 0x0A
        self.sensor.acc_int_map_data = 0x04
        self.sensor.gyro_range = 0x03
        self.sensor.gyro_bandwidth = 0x01
        self.sensor.gyro_lpm1 = 0x00
        self.sensor.gyro_int3_int4_io_map = 0x01
        self.sensor.gyro_int3_int4_io_conf = 0x51
        self.sensor.gyro_int_ctrl = 0x80
        time.sleep(0.02)
        if self.is_i2c_configured:
            return self._configure_i2c_interrupt_streaming()
        if self.is_spi_configured:
            return self._configure_spi_interrupt_streaming()
        error_message = "Configure I2C or SPI protocol first"
        raise BMI088ShuttleError(error_message)

    def start_streaming(self) -> None:
        if self.is_polling_streaming_configured:
            return self.board.start_polling_streaming()
        if self.is_interrupt_streaming_configured:
            return self.board.start_interrupt_streaming()
        error_message = "Configure polling or interrupt streaming before streaming start"
        raise BMI088ShuttleError(error_message)

    def stop_streaming(self) -> None:
        self.board.stop_polling_streaming()
        time.sleep(0.15)
        self.board.stop_interrupt_streaming()

    def decode_gyro_streaming(self, payload: array[int]) -> BMI088GyroPacket:
        g_x, g_y, g_z = struct.unpack("<hhh", payload)
        return BMI088GyroPacket(g_x_raw=g_x, g_y_raw=g_y, g_z_raw=g_z)

    def decode_accel_streaming(self, payload: array[int]) -> BMI088AccelPacket:
        if self.is_spi_configured and len(payload) == 7:
            a_x, a_y, a_z = struct.unpack("<xhhh", payload)
            return BMI088AccelPacket(a_x_raw=a_x, a_y_raw=a_y, a_z_raw=a_z)
        if self.is_i2c_configured:
            a_x, a_y, a_z = struct.unpack("<hhh", payload)
            return BMI088AccelPacket(a_x_raw=a_x, a_y_raw=a_y, a_z_raw=a_z)
        error_message = f"Cannot parse payload={payload} of length={len(payload)}"
        raise BMI088ShuttleError(error_message)
