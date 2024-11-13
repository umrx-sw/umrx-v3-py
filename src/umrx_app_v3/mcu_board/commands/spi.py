import logging
import struct
from array import array
from collections.abc import Generator

from umrx_app_v3.mcu_board.bst_protocol_constants import (
    CommandId,
    CommandType,
    InterfaceSDO,
    MultiIOPin,
    SensorInterface,
    SPIBus,
    SPIMode,
    SPISpeed,
    SPITransfer,
    StreamingDDMode,
)
from umrx_app_v3.mcu_board.commands.command import Command, CommandError

logger = logging.getLogger(__name__)


class SPICmd(Command):
    DefaultSPIBus = SPIBus.BUS_0
    DefaultSPIMode = SPIMode.MODE_3

    @staticmethod
    def set_bus(bus: SPIBus) -> None:
        SPICmd.DefaultSPIBus = bus

    @staticmethod
    def set_mode(mode: SPIMode) -> None:
        SPICmd.DefaultSPIMode = mode


class SPIConfigureCmd(SPICmd):
    @staticmethod
    def assemble(speed: SPISpeed = SPISpeed.MHz_5) -> Generator:
        yield SPIConfigureCmd.config()
        yield SPIConfigureCmd.set_speed(speed)

    @staticmethod
    def config() -> array[int]:
        payload = (
            CommandType.DD_SET.value,
            CommandId.INTERFACE.value,
            SensorInterface.SPI.value,
            InterfaceSDO.SDO_LOW.value,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def set_speed(speed: SPISpeed) -> array[int]:
        payload = (
            CommandType.DD_SET.value,
            CommandId.SPI_SETTINGS.value,
            SPICmd.DefaultSPIBus.value,
            SPICmd.DefaultSPIMode.value,
            SPITransfer.SPI_8BIT.value,
            speed.value,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> None:
        if not Command.check_message(message):
            error_message = f"Cannot parse invalid message {message}"
            raise CommandError(error_message)


class SPIReadCmd(SPICmd):
    @staticmethod
    def assemble(cs_pin: MultiIOPin, register_address: int, bytes_to_read: int) -> array[int]:
        sensor_id, analog_switch = 1, 1
        device_address = 0, 0
        bytes_to_read_serialized = (int(a) for a in struct.pack(">H", bytes_to_read))
        write_only_once = 1
        delay_between_writes = 0
        read_response = 1
        payload = (
            CommandType.DD_GET.value,
            CommandId.SENSOR_WRITE_AND_READ.value,
            StreamingDDMode.BURST_MODE.value,
            cs_pin.value,
            sensor_id,
            analog_switch,
            *device_address,
            register_address | 0x80,
            *bytes_to_read_serialized,
            write_only_once,
            delay_between_writes,
            read_response,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> array[int]:
        return Command.parse_read_response(message)


class SPIWriteCmd(Command):
    @staticmethod
    def assemble(cs_pin: MultiIOPin, start_register_address: int, data_to_write: array[int]) -> array[int]:
        ok, message = Command.check_for_max_payload(data_to_write)
        if not ok:
            raise CommandError(message)
        sensor_id, analog_switch = 1, 1
        device_address = 0, 0
        write_only_once = 1
        delay_between_writes = 0
        read_response = 0
        payload = (
            CommandType.DD_SET.value,
            CommandId.SENSOR_WRITE_AND_READ.value,
            StreamingDDMode.BURST_MODE.value,
            cs_pin.value,
            sensor_id,
            analog_switch,
            *device_address,
            start_register_address & 0x7F,
            0,
            len(data_to_write),
            write_only_once,
            delay_between_writes,
            read_response,
            *data_to_write,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> None: ...
