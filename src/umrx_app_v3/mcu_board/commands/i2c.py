import logging
import struct
from array import array
from collections.abc import Generator

from umrx_app_v3.mcu_board.bst_protocol_constants import (
    CoinesResponse,
    CommandId,
    CommandType,
    ErrorCode,
    I2CBus,
    I2CMode,
    InterfaceSDO,
    SensorInterface,
    StreamingDDMode,
)
from umrx_app_v3.mcu_board.commands.command import Command, CommandError

logger = logging.getLogger(__name__)


class I2CCmd(Command):
    DefaultI2CBus = I2CBus.BUS_I2C_0

    @staticmethod
    def set_bus(bus: I2CBus) -> None:
        I2CCmd.DefaultI2CBus = bus


class I2CConfigureCmd(I2CCmd):
    @staticmethod
    def assemble(speed: I2CMode = I2CMode.STANDARD_MODE) -> Generator:
        yield I2CConfigureCmd.config()
        yield I2CConfigureCmd.set_speed(speed)

    @staticmethod
    def config() -> array[int]:
        payload = (
            CommandType.DD_SET.value,
            CommandId.INTERFACE.value,
            SensorInterface.I2C.value,
            InterfaceSDO.SDO_LOW.value,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def set_speed(speed: I2CMode) -> array[int]:
        payload = (
            CommandType.DD_SET.value,
            CommandId.I2C_SPEED.value,
            I2CConfigureCmd.DefaultI2CBus.value,
            speed.value,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> None: ...


class I2CReadCmd(I2CCmd):
    @staticmethod
    def assemble(i2c_address: int, register_address: int, bytes_to_read: int) -> array[int]:
        i2c_interface = 0
        sensor_id, analog_switch = 1, 1
        i2c_address_serialized = (int(a) for a in struct.pack(">H", i2c_address))
        bytes_to_read_serialized = (int(a) for a in struct.pack(">H", bytes_to_read))
        write_only_once = 1
        delay_between_writes = 0
        read_response = 1
        payload = (
            CommandType.DD_GET.value,
            CommandId.SENSOR_WRITE_AND_READ.value,
            StreamingDDMode.BURST_MODE.value,
            i2c_interface,
            sensor_id,
            analog_switch,
            *i2c_address_serialized,
            register_address,
            *bytes_to_read_serialized,
            write_only_once,
            delay_between_writes,
            read_response,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> array[int]:
        if not Command.check_message(message):
            error_message = f"Cannot parse invalid message {message}"
            raise CommandError(error_message)
        message_len = message[1]
        message_feature = message[CoinesResponse.DD_RESPONSE_FEATURE_POSITION.value]
        feature_correct = message_feature == CommandId.SENSOR_WRITE_AND_READ.value
        message_status = message[CoinesResponse.DD_RESPONSE_STATUS_POSITION.value]
        status_ok = message_status == ErrorCode.SUCCESS.value
        if not (feature_correct and status_ok):
            error_message = f"Error in message: {feature_correct=}, {status_ok=}, {message=}"
            raise CommandError(error_message)

        extended_read_idx = CoinesResponse.DD_RESPONSE_COMMAND_ID_POSITION.value
        if message[extended_read_idx] == CoinesResponse.DD_RESPONSE_EXTENDED_READ_ID.value:
            payload_msb = message[CoinesResponse.DD_RESPONSE_PACKET_LENGTH_MSB_POSITION.value]
            payload_lsb = message[CoinesResponse.DD_RESPONSE_PACKET_LENGTH_LSB_POSITION.value]
            payload_len = (payload_msb << 8) | payload_lsb
        else:
            payload_len = message_len - CoinesResponse.DD_RESPONSE_OVERHEAD_BYTES.value

        payload_start = CoinesResponse.DD_RESPONSE_OVERHEAD_BYTES.value - 2
        return array("B", (int(el) for el in message[payload_start : payload_start + payload_len]))
