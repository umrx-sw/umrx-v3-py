import logging
import struct
from array import array
from collections.abc import Generator
from dataclasses import dataclass, field
from typing import Literal

from umrx_app_v3.mcu_board.bst_protocol_constants import (
    CoinesInterruptStreamResponse,
    CoinesResponse,
    CommandType,
    ErrorCode,
    MultiIOPin,
    StreamingDataResponse,
)
from umrx_app_v3.mcu_board.commands.command import Command, CommandError

logger = logging.getLogger(__name__)


@dataclass
class StreamingInterruptSpiChannelConfig:
    id: int | None = None
    interrupt_pin: MultiIOPin | None = None
    cs_pin: MultiIOPin | None = None
    register_address: int | None = None
    bytes_to_read: int | None = None


@dataclass
class StreamingInterruptI2cChannelConfig:
    id: int | None = None
    interrupt_pin: MultiIOPin | None = None
    i2c_address: int | None = None
    register_address: int | None = None
    bytes_to_read: int | None = None


@dataclass
class StreamingInterruptSpiConfig:
    channel_configs: list[StreamingInterruptSpiChannelConfig] = field(default_factory=list)


@dataclass
class StreamingInterruptI2cConfig:
    channel_configs: list[StreamingInterruptI2cChannelConfig] = field(default_factory=list)


class StreamingInterruptCmd(Command):
    streaming_interrupt_config: StreamingInterruptSpiConfig | StreamingInterruptI2cConfig | None = None

    @staticmethod
    def assemble(sensor_interface: Literal["spi", "i2c"]) -> Generator:
        if sensor_interface == "spi":
            return StreamingInterruptCmd.configure_spi()
        if sensor_interface == "i2c":
            return StreamingInterruptCmd.configure_i2c()
        error_message = f"Unknown interface {sensor_interface}"
        raise CommandError(error_message)

    @staticmethod
    def parse(message: array[int]) -> tuple[int, int, int, array[int]]:
        return StreamingInterruptCmd.parse_streaming_packet(message)

    @staticmethod
    def set_spi_config() -> None:
        StreamingInterruptCmd.streaming_interrupt_config = StreamingInterruptSpiConfig()

    @staticmethod
    def reset_spi_config() -> None:
        StreamingInterruptCmd.set_spi_config()

    @staticmethod
    def set_i2c_config() -> None:
        StreamingInterruptCmd.streaming_interrupt_config = StreamingInterruptI2cConfig()

    @staticmethod
    def reset_i2c_config() -> None:
        StreamingInterruptCmd.set_i2c_config()

    @staticmethod
    def start_streaming() -> array[int]:
        infinite_samples = 0xFF
        payload = (CommandType.DD_START_STOP_STREAMING_INTERRUPT.value, infinite_samples)
        return Command.create_message_from(payload)

    @staticmethod
    def stop_streaming() -> array[int]:
        num_samples = 0
        payload = (CommandType.DD_START_STOP_STREAMING_INTERRUPT.value, num_samples)
        return Command.create_message_from(payload)

    @staticmethod
    def configure_spi() -> Generator:
        for config in StreamingInterruptCmd.streaming_interrupt_config.channel_configs:
            yield StreamingInterruptCmd.assemble_spi_channel_config(config)

    @staticmethod
    def configure_i2c() -> Generator:
        for config in StreamingInterruptCmd.streaming_interrupt_config.channel_configs:
            yield StreamingInterruptCmd.assemble_i2c_channel_config(config)

    @staticmethod
    def set_streaming_channel_spi(
        interrupt_pin: MultiIOPin,
        cs_pin: MultiIOPin,
        register_address: int,
        bytes_to_read: int,
    ) -> None:
        if StreamingInterruptCmd.streaming_interrupt_config is None:
            StreamingInterruptCmd.set_spi_config()
        channel_id = len(StreamingInterruptCmd.streaming_interrupt_config.channel_configs) + 1
        config = StreamingInterruptSpiChannelConfig(
            id=channel_id,
            interrupt_pin=interrupt_pin,
            cs_pin=cs_pin,
            register_address=register_address,
            bytes_to_read=bytes_to_read,
        )
        StreamingInterruptCmd.streaming_interrupt_config.channel_configs.append(config)

    @staticmethod
    def assemble_spi_channel_config(channel_config: StreamingInterruptSpiChannelConfig) -> array[int]:
        device_address = 0, 0
        interrupt_timestamp = 1
        num_blocks = 1
        interrupt_timeout = 0xF0, 0xF0
        payload = (
            CommandType.DD_CONFIG_STREAM_INTERRUPT.value,
            channel_config.id,
            interrupt_timestamp,
            channel_config.cs_pin.value,
            channel_config.interrupt_pin.value,
            *device_address,
            1,
            num_blocks,
            channel_config.register_address,
            0,
            channel_config.bytes_to_read,
            *interrupt_timeout,
            0,
            0,
            0,
            0,
            0,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def set_streaming_channel_i2c(
        interrupt_pin: MultiIOPin,
        i2c_address: int,
        register_address: int,
        bytes_to_read: int,
    ) -> None:
        if StreamingInterruptCmd.streaming_interrupt_config is None:
            StreamingInterruptCmd.set_i2c_config()
        channel_id = len(StreamingInterruptCmd.streaming_interrupt_config.channel_configs) + 1
        config = StreamingInterruptI2cChannelConfig(
            id=channel_id,
            interrupt_pin=interrupt_pin,
            i2c_address=i2c_address,
            register_address=register_address,
            bytes_to_read=bytes_to_read,
        )
        StreamingInterruptCmd.streaming_interrupt_config.channel_configs.append(config)

    @staticmethod
    def assemble_i2c_channel_config(channel_config: StreamingInterruptI2cChannelConfig) -> array[int]:
        interrupt_timestamp = 1
        i2c_interface = 0
        i2c_address = (int(el) for el in struct.pack(">H", channel_config.i2c_address))
        num_blocks = 1
        interrupt_timeout = 0xF0, 0xF0
        payload = (
            CommandType.DD_CONFIG_STREAM_INTERRUPT.value,
            channel_config.id,
            interrupt_timestamp,
            i2c_interface,
            channel_config.interrupt_pin.value,
            *i2c_address,
            1,
            num_blocks,
            channel_config.register_address,
            0,
            channel_config.bytes_to_read,
            *interrupt_timeout,
            0,
            0,
            0,
            0,
            0,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def parse_streaming_packet(
        message: array[int], *, includes_mcu_timestamp: bool = False
    ) -> tuple[int, int, int, array[int]]:
        if not Command.check_message(message):
            error_message = f"Cannot parse invalid message {message}"
            raise CommandError(error_message)
        message_status = message[CoinesResponse.DD_RESPONSE_STATUS_POSITION.value]
        message_feature = message[CoinesResponse.DD_RESPONSE_COMMAND_ID_POSITION.value]
        feature_correct = message_feature == StreamingDataResponse.INTERRUPT.value
        status_ok = message_status == ErrorCode.SUCCESS.value
        if not (feature_correct and status_ok):
            error_message = f"Error in message: {feature_correct=}, {status_ok=}, {message=}"
            raise CommandError(error_message)

        message_channel_id = message[CoinesInterruptStreamResponse.CHANNEL_ID_IDX.value]
        packet_count_start = CoinesInterruptStreamResponse.PACKET_COUNT_IDX.value
        packet_count_end = CoinesInterruptStreamResponse.PACKET_COUNT_LENGTH.value + packet_count_start
        packet_count_raw = message[packet_count_start:packet_count_end]
        (packet_count,) = struct.unpack(">I", packet_count_raw)
        time_stamp = -1
        if includes_mcu_timestamp:
            payload_end = CoinesInterruptStreamResponse.TIME_STAMP_IDX.value
            time_stamp_start = CoinesInterruptStreamResponse.TIME_STAMP_IDX.value
            time_stamp_end = CoinesInterruptStreamResponse.PACKET_FOOTER.value
            time_stamp_raw = message[time_stamp_start:time_stamp_end]
            time_stamp = array("B", (0, 0)) + array("B", time_stamp_raw)
            (time_stamp,) = struct.unpack(">Q", time_stamp)
            time_stamp = time_stamp // 30  # time stamp in micro-seconds
        else:
            payload_end = CoinesInterruptStreamResponse.PACKET_FOOTER.value
        payload = message[CoinesInterruptStreamResponse.PAYLOAD_START_IDX.value : payload_end]
        payload_array = array("B", (int(el) for el in payload))
        return message_channel_id, packet_count, time_stamp, payload_array
