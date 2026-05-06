import logging
import struct
import time
from array import array
from pathlib import Path
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
from umrx_app_v3.sensors.bhi360 import BHI360, BHI360Addr, BHI360CommandId

logger = logging.getLogger(__name__)


class BHI360ShuttleError(Exception): ...


class BHI360Shuttle:
    # 1-wire PROM
    SHUTTLE_ID = 0x179
    # Pins
    SDO = MultiIOPin.MINI_SHUTTLE_PIN_2_3
    CS = MultiIOPin.MINI_SHUTTLE_PIN_2_1
    INT1 = MultiIOPin.MINI_SHUTTLE_PIN_1_6
    RESETN = MultiIOPin.MINI_SHUTTLE_PIN_1_5
    # I2C addresses
    I2C_ADDRESS_SDO_HIGH = 0x29
    I2C_ADDRESS_SDO_LOW = 0x28
    # Firmware
    FIRMWARE_MAGIC = 0x662B

    def __init__(self, **kw: Any) -> None:
        self.board: ApplicationBoard | None = kw["board"] if kw.get("board") else None
        self.sensor: BHI360 = BHI360()
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
            raise BHI360ShuttleError(error_message)

    def assign_sensor_callbacks(self) -> None:
        self.sensor.assign_callbacks(read_callback=self.read_register, write_callback=self.write_register)

    def configure_i2c(self) -> None:
        self.board.set_pin_config(self.SDO, PinDirection.OUTPUT, PinValue.LOW)
        self.board.set_pin_config(self.CS, PinDirection.OUTPUT, PinValue.HIGH)
        time.sleep(0.01)
        self.board.set_vdd_vddio(1.8, 1.8)
        time.sleep(0.1)
        self.board.set_pin_config(self.RESETN, PinDirection.OUTPUT, PinValue.HIGH)
        self.board.set_pin_config(self.INT1, PinDirection.INPUT, PinValue.LOW)
        self.board.configure_i2c(I2CMode.SPEED_3_4_MHZ)

        self.assign_sensor_callbacks()
        self.is_i2c_configured = True
        self.is_spi_configured = False

    def configure_spi(self) -> None:
        # self.board.set_vdd_vddio(0.0, 0.0)
        # time.sleep(0.1)
        self.board.set_pin_config(self.CS, PinDirection.OUTPUT, PinValue.HIGH)
        self.board.set_vdd_vddio(1.8, 1.8)
        time.sleep(0.2)
        if isinstance(self.board, ApplicationBoardV3Rev1):
            SPIConfigureCmd.set_bus(SPIBus.BUS_1)
        self.board.configure_spi()
        self.assign_sensor_callbacks()
        self.is_spi_configured = True
        self.is_i2c_configured = False

    def read_register(self, reg_addr: int, bytes_to_read: int = 1) -> array[int] | int:
        if isinstance(reg_addr, BHI360Addr):
            reg_addr = reg_addr.value
        if self.is_i2c_configured:
            values = self.board.read_i2c(self.I2C_ADDRESS_SDO_LOW, reg_addr, bytes_to_read)
            if bytes_to_read == 1:
                return values[0]
            return values
        if self.is_spi_configured:
            if bytes_to_read == 1:
                return self.read_single_register_spi(reg_addr)
            return self.read_multiple_spi(reg_addr, bytes_to_read)

        error_message = "Configure I2C or SPI protocol prior to reading registers"
        raise BHI360ShuttleError(error_message)

    def read_single_register_spi(self, reg_addr: int) -> int:
        values = self.board.read_spi(self.CS, reg_addr, 2)
        return values[1]

    def read_multiple_spi(self, start_register_addr: int, bytes_to_read: int) -> array[int]:
        values = self.board.read_spi(self.CS, start_register_addr, bytes_to_read + 1)
        return values[1:]

    def write_register(self, reg_addr: int, value: int | array) -> None:
        if isinstance(reg_addr, BHI360Addr):
            reg_addr = reg_addr.value
        if self.is_i2c_configured:
            if isinstance(value, array):
                return self.board.write_i2c(self.I2C_ADDRESS_SDO_LOW, reg_addr, value)
            return self.board.write_i2c(self.I2C_ADDRESS_SDO_LOW, reg_addr, array("B", (value,)))
        if self.is_spi_configured:
            if isinstance(value, array):
                return self.board.write_spi(self.CS, reg_addr, value)
            return self.board.write_spi(self.CS, reg_addr, array("B", (value,)))
        error_message = "Configure I2C or SPI protocol prior to reading registers"
        raise BHI360ShuttleError(error_message)

    def _configure_i2c_polling_streaming(
        self,
        sampling_time: int,
        sampling_unit: StreamingSamplingUnit,
    ) -> None:
        self.board.streaming_polling_set_i2c_channel(
            i2c_address=self.I2C_ADDRESS_SDO_LOW,
            sampling_time=sampling_time,
            sampling_unit=sampling_unit,
            register_address=BHI360Addr.acc_data_0.value,
            bytes_to_read=(6 + 1 + 3),
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
            register_address=BHI360Addr.acc_data_0.value,
            bytes_to_read=(1 + 6 + 1 + 3),
        )
        self.board.configure_streaming_polling(interface="spi")
        self.is_polling_streaming_configured = True

    def configure_polling_streaming(
        self,
        sampling_time: int = 1,
        sampling_unit: StreamingSamplingUnit = StreamingSamplingUnit.MILLI_SECOND,
    ) -> None:
        if self.is_i2c_configured:
            return self._configure_i2c_polling_streaming(sampling_time, sampling_unit)
        if self.is_spi_configured:
            return self._configure_spi_polling_streaming(sampling_time, sampling_unit)
        error_message = "Configure I2C or SPI protocol first"
        raise BHI360ShuttleError(error_message)

    def _configure_i2c_interrupt_streaming(self) -> None:
        self.board.streaming_interrupt_set_i2c_channel(
            interrupt_pin=self.INT1,
            i2c_address=BHI360Shuttle.I2C_ADDRESS_SDO_LOW,
            register_address=BHI360Addr.acc_data_0.value,
            bytes_to_read=(6 + 1 + 3),
        )
        self.board.configure_streaming_interrupt(interface="i2c")
        self.is_interrupt_streaming_configured = True

    def configure_interrupt_streaming(self) -> None:
        time.sleep(0.02)
        if self.is_i2c_configured:
            return self._configure_i2c_interrupt_streaming()
        error_message = "Configure I2C protocol first. SPI interrupt streaming is not supported for this shuttle."
        raise BHI360ShuttleError(error_message)

    def start_streaming(self) -> None:
        if self.is_polling_streaming_configured:
            return self.board.start_polling_streaming()
        if self.is_interrupt_streaming_configured:
            return self.board.start_interrupt_streaming()
        error_message = "Configure polling or interrupt streaming before streaming start"
        raise BHI360ShuttleError(error_message)

    def stop_streaming(self) -> None:
        self.board.stop_polling_streaming()
        time.sleep(0.15)
        self.board.stop_interrupt_streaming()

    def upload_firmware_to_ram(self, file_path: Path) -> None:
        firmware_content = self.get_firmware_bytes(file_path)
        self.upload_to_ram(firmware_content)

    @staticmethod
    def read_firmware_file(file_path: Path) -> bytes:
        with open(file_path, "rb") as fd:
            firmware_content = fd.read()
        firmware_header = struct.unpack("<I", firmware_content[0:4])[0]
        if firmware_header != BHI360Shuttle.FIRMWARE_MAGIC:
            error_message = f"Invalid format: must start with magic {firmware_header}!={BHI360Shuttle.FIRMWARE_MAGIC}!"
            raise BHI360ShuttleError(error_message)
        if len(firmware_content) > 2 ** 18:
            error_message = "Invalid firmware: too big, will not fit in RAM"
            raise BHI360ShuttleError(error_message)
        if len(firmware_content) % 4 != 0:
            firmware_content += bytes(len(firmware_content) % 4)
        return firmware_content

    def get_firmware_bytes(self, file_path: Path) -> bytes:
        firmware_content = self.read_firmware_file(file_path)
        header = struct.pack("<HH", *(BHI360CommandId.upload_to_program_ram.value, len(firmware_content) // 4))
        return header + firmware_content

    def upload_to_ram(self, firmware_bytes: bytes) -> None:
        transaction_length = 40
        for i in range(0, len(firmware_bytes), transaction_length):
            chunk_data = firmware_bytes[i : i + transaction_length]
            # logger.info(f"writing chunk of {len(chunk_data)} bytes")
            chunk = array("B", chunk_data)
            if self.is_i2c_configured:
                self.board.write_i2c(self.I2C_ADDRESS_SDO_LOW, BHI360Addr.chan_cmd.value, chunk)
            if self.is_spi_configured:
                self.board.write_spi(self.CS, BHI360Addr.chan_cmd.value, chunk)
        if not (self.is_spi_configured or self.is_i2c_configured):
            error_message = "Configure I2C or SPI protocol prior to writing configuration file"
            raise BHI360ShuttleError(error_message)

    def boot_program_ram(self) -> None:
        command = struct.pack("<HH", *(BHI360CommandId.boot_program_ram.value, 0))
        if self.is_i2c_configured:
            self.board.write_i2c(self.I2C_ADDRESS_SDO_LOW, BHI360Addr.chan_cmd.value, command)
        if self.is_spi_configured:
            self.board.write_spi(self.CS, BHI360Addr.chan_cmd.value, command)
        if not (self.is_spi_configured or self.is_i2c_configured):
            error_message = "Configure I2C or SPI protocol prior to writing configuration file"
            raise BHI360ShuttleError(error_message)

    def read_parameter(self, command: int) -> None:
        command  = struct.pack("<HH", *(command | 0x1000, 0))
        if self.is_i2c_configured:
            self.board.write_i2c(self.I2C_ADDRESS_SDO_LOW, BHI360Addr.chan_cmd.value, command)
        if self.is_spi_configured:
            self.board.write_spi(self.CS, BHI360Addr.chan_cmd.value, command)
        if not (self.is_spi_configured or self.is_i2c_configured):
            error_message = "Configure I2C or SPI protocol prior to writing configuration file"
            raise BHI360ShuttleError(error_message)

    def read_from_fifo(self, num_bytes: int) -> bytes:
        if self.is_i2c_configured:
            return self.board.read_i2c(self.I2C_ADDRESS_SDO_LOW, BHI360Addr.chan_status.value, num_bytes)
        if self.is_spi_configured:
            return self.board.read_spi(self.CS, BHI360Addr.chan_status.value, num_bytes)

    def firmware_version(self) -> tuple[int,...]:
        firmware_version_parameter = 0x0104
        self.read_parameter(firmware_version_parameter)
        values = self.read_from_fifo(24)

        command, payload_length = struct.unpack("<HH", values[0:4])
        assert command == firmware_version_parameter, "Invalid command {}".format(command)
        assert payload_length == 20, "Invalid response length"
        custom_version, em_hash1, em_hash2, bst_hash1, bst_hash2, user_hash1, user_hash2 = struct.unpack("<HIHIHIH", values[4:])
        em_hash = em_hash2 << 32 | em_hash1
        bst_hash = bst_hash2 << 32 | bst_hash1
        user_hash = user_hash2 << 32 | user_hash1
        return custom_version, em_hash, bst_hash, user_hash

    def virtual_sensors_present(self) -> tuple[int,...]:
        virtual_sensor_parameter = 0x011F
        self.read_parameter(virtual_sensor_parameter)
        values = self.read_from_fifo(36)

        command, payload_length = struct.unpack("<HH", values[0:4])
        assert command == virtual_sensor_parameter, "Invalid command {}".format(command)
        assert payload_length == 32, "Invalid response length"
        return values[4:]

    def physical_sensors_present(self) -> tuple[int,...]:
        physical_sensor_parameter = 0x0120
        self.read_parameter(physical_sensor_parameter)
        values = self.read_from_fifo(12)

        command, payload_length = struct.unpack("<HH", values[0:4])
        assert command == physical_sensor_parameter, "Invalid command {}".format(command)
        assert payload_length == 8, "Invalid response length"
        return values[4:]

    def time_stamps(self) -> tuple[float,...]:
        time_stamps_parameter = 0x0105
        self.read_parameter(time_stamps_parameter)
        values = self.read_from_fifo(20)

        command, payload_length = struct.unpack("<HH", values[0:4])
        assert command == time_stamps_parameter, "Invalid command {}".format(command)
        assert payload_length == 16, "Invalid response length"
        host_int_ts1, host_int_ts2, cur_ts1, cur_ts2, event_ts1, event_ts2 = struct.unpack("<IBIBIBx", values[4:])
        host_int_ts = (host_int_ts2 << 32) | host_int_ts1
        cur_ts = (cur_ts2 << 32) | cur_ts1
        event_ts = (event_ts2 << 32) | event_ts1
        host_int_ts *=  1 / 64000
        cur_ts *= 1 / 64000
        event_ts *= 1 / 64000
        return host_int_ts, cur_ts, event_ts