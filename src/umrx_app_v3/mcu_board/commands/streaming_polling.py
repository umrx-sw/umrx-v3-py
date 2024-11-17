import logging
import math
import struct
from array import array
from collections.abc import Generator
from dataclasses import dataclass, field
from typing import Literal

from umrx_app_v3.mcu_board.bst_protocol_constants import (
    CoinesPollingStreamResponse,
    CoinesResponse,
    CommandType,
    ErrorCode,
    MultiIOPin,
    StreamingDataResponse,
    StreamingSamplingUnit,
)
from umrx_app_v3.mcu_board.commands.command import Command, CommandError

logger = logging.getLogger(__name__)


@dataclass
class PollingStreamingSpiChannelConfig:
    id: int | None = None
    cs_pin: MultiIOPin | None = None
    sampling_time: int | None = None
    sampling_unit: StreamingSamplingUnit | None = None
    register_address: int | None = None
    bytes_to_read: int | None = None


@dataclass
class PollingStreamingI2cChannelConfig:
    id: int | None = None
    i2c_address: int | None = None
    sampling_time: int | None = None
    sampling_unit: StreamingSamplingUnit | None = None
    register_address: int | None = None
    bytes_to_read: int | None = None


@dataclass
class PollingStreamingSpiConfig:
    channel_configs: list[PollingStreamingSpiChannelConfig] = field(default_factory=list)


@dataclass
class PollingStreamingI2cConfig:
    channel_configs: list[PollingStreamingI2cChannelConfig] = field(default_factory=list)


class StreamingPollingCmd(Command):
    polling_streaming_config: PollingStreamingSpiConfig | PollingStreamingI2cConfig | None = None

    @staticmethod
    def assemble(sensor_interface: Literal["spi", "i2c"]) -> Generator:
        if sensor_interface == "spi":
            return StreamingPollingCmd.configure_spi()
        if sensor_interface == "i2c":
            return StreamingPollingCmd.configure_i2c()
        error_message = f"Unknown interface {sensor_interface}"
        raise CommandError(error_message)

    @staticmethod
    def parse(message: array[int]) -> tuple[int, array[int]]:
        return StreamingPollingCmd.parse_streaming_packet(message)

    @staticmethod
    def set_spi_config() -> None:
        StreamingPollingCmd.polling_streaming_config = PollingStreamingSpiConfig()

    @staticmethod
    def reset_spi_config() -> None:
        StreamingPollingCmd.set_spi_config()

    @staticmethod
    def set_i2c_config() -> None:
        StreamingPollingCmd.polling_streaming_config = PollingStreamingI2cConfig()

    @staticmethod
    def reset_i2c_config() -> None:
        StreamingPollingCmd.set_i2c_config()

    @staticmethod
    def start_streaming() -> array[int]:
        infinite_samples = 0xFF
        payload = (CommandType.DD_START_STOP_STREAMING_POLLING.value, infinite_samples)
        return Command.create_message_from(payload)

    @staticmethod
    def stop_streaming() -> array[int]:
        num_samples = 0
        payload = (CommandType.DD_START_STOP_STREAMING_POLLING.value, num_samples)
        return Command.create_message_from(payload)

    @staticmethod
    def configure_spi() -> Generator:
        yield StreamingPollingCmd.set_sampling_time()
        for config in StreamingPollingCmd.polling_streaming_config.channel_configs:
            yield StreamingPollingCmd.assemble_spi_channel_config(config)

    @staticmethod
    def configure_i2c() -> Generator:
        yield StreamingPollingCmd.set_sampling_time()
        for config in StreamingPollingCmd.polling_streaming_config.channel_configs:
            yield StreamingPollingCmd.assemble_i2c_channel_config(config)

    @staticmethod
    def set_sampling_time_direct(
        number_of_sensors: int, sampling_time: int, sampling_unit: StreamingSamplingUnit
    ) -> array[int]:
        if number_of_sensors > 2:
            message = f"Exceeds max supported number of sensors (2), attempted: {number_of_sensors}"
            raise CommandError(message)
        payload = (
            CommandType.DD_STREAMING_SETTINGS.value,
            number_of_sensors,
            1,
            *(int(el) for el in struct.pack(">H", sampling_time)),
            sampling_unit.value,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def set_sampling_time() -> array[int]:
        number_of_sensors = len(StreamingPollingCmd.polling_streaming_config.channel_configs)
        if number_of_sensors > 2:
            message = f"Exceeds max supported number of sensors = 2, attempted: {number_of_sensors}"
            raise CommandError(message)

        if number_of_sensors == 2:
            streaming_time_1 = StreamingPollingCmd.polling_streaming_config.channel_configs[0].sampling_time
            streaming_unit_1 = StreamingPollingCmd.polling_streaming_config.channel_configs[0].sampling_unit

            streaming_time_2 = StreamingPollingCmd.polling_streaming_config.channel_configs[1].sampling_time
            streaming_unit_2 = StreamingPollingCmd.polling_streaming_config.channel_configs[1].sampling_unit

            if streaming_unit_1 != StreamingSamplingUnit.MICRO_SECOND:
                streaming_time_1 = streaming_time_1 * 1000
            if streaming_unit_2 != StreamingSamplingUnit.MICRO_SECOND:
                streaming_time_2 = streaming_time_2 * 1000

            sampling_time = math.gcd(streaming_time_1, streaming_time_2)
            sampling_unit = StreamingSamplingUnit.MICRO_SECOND
            if sampling_time > 1000:
                sampling_time //= 1000
                sampling_unit = StreamingSamplingUnit.MILLI_SECOND
        elif number_of_sensors == 1:
            sampling_time = StreamingPollingCmd.polling_streaming_config.channel_configs[0].sampling_time
            sampling_unit = StreamingPollingCmd.polling_streaming_config.channel_configs[0].sampling_unit
        else:
            error_msg = "Specify streaming configuration first, call set_streaming_channel_[i2c|spi] before!"
            raise CommandError(error_msg)
        return StreamingPollingCmd.set_sampling_time_direct(
            number_of_sensors=number_of_sensors, sampling_time=sampling_time, sampling_unit=sampling_unit
        )

    @staticmethod
    def set_streaming_channel_spi(
        cs_pin: MultiIOPin,
        sampling_time: int,
        sampling_unit: StreamingSamplingUnit,
        register_address: int,
        bytes_to_read: int,
    ) -> None:
        if StreamingPollingCmd.polling_streaming_config is None:
            StreamingPollingCmd.set_spi_config()
        channel_id = len(StreamingPollingCmd.polling_streaming_config.channel_configs) + 1
        config = PollingStreamingSpiChannelConfig(
            id=channel_id,
            cs_pin=cs_pin,
            sampling_time=sampling_time,
            sampling_unit=sampling_unit,
            register_address=register_address,
            bytes_to_read=bytes_to_read,
        )
        StreamingPollingCmd.polling_streaming_config.channel_configs.append(config)

    @staticmethod
    def assemble_spi_channel_config(channel_config: PollingStreamingSpiChannelConfig) -> array[int]:
        analog_switch = 1
        device_address = 0, 0
        num_blocks = 1
        payload = (
            CommandType.DD_CONFIG_STREAM_POLLING.value,
            channel_config.id,
            0,
            channel_config.cs_pin.value,
            analog_switch,
            *device_address,
            *(int(el) for el in struct.pack(">H", channel_config.sampling_time)),
            channel_config.sampling_unit.value,
            1,
            num_blocks,
            channel_config.register_address,
            0,
            channel_config.bytes_to_read,
            0,
            0,
            0,
            0,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def set_streaming_channel_i2c(
        i2c_address: int,
        sampling_time: int,
        sampling_unit: StreamingSamplingUnit,
        register_address: int,
        bytes_to_read: int,
    ) -> None:
        if StreamingPollingCmd.polling_streaming_config is None:
            StreamingPollingCmd.set_i2c_config()
        channel_id = len(StreamingPollingCmd.polling_streaming_config.channel_configs) + 1
        config = PollingStreamingI2cChannelConfig(
            id=channel_id,
            i2c_address=i2c_address,
            sampling_time=sampling_time,
            sampling_unit=sampling_unit,
            register_address=register_address,
            bytes_to_read=bytes_to_read,
        )
        StreamingPollingCmd.polling_streaming_config.channel_configs.append(config)

    @staticmethod
    def assemble_i2c_channel_config(channel_config: PollingStreamingI2cChannelConfig) -> array[int]:
        analog_switch = 1
        i2c_interface = 0
        i2c_address = (int(el) for el in struct.pack(">H", channel_config.i2c_address))
        num_blocks = 1
        payload = (
            CommandType.DD_CONFIG_STREAM_POLLING.value,
            channel_config.id,
            0,
            i2c_interface,
            analog_switch,
            *i2c_address,
            *(int(el) for el in struct.pack(">H", channel_config.sampling_time)),
            channel_config.sampling_unit.value,
            1,
            num_blocks,
            channel_config.register_address,
            0,
            channel_config.bytes_to_read,
            0,
            0,
            0,
            0,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def parse_streaming_packet(message: array[int]) -> tuple[int, array[int]]:
        if not Command.check_message(message):
            error_message = f"Cannot parse invalid message {message}"
            raise CommandError(error_message)
        message_status = message[CoinesResponse.DD_RESPONSE_STATUS_POSITION.value]
        message_feature = message[CoinesResponse.DD_RESPONSE_COMMAND_ID_POSITION.value]
        feature_correct = message_feature == StreamingDataResponse.POLLING.value
        status_ok = message_status == ErrorCode.SUCCESS.value
        if not (feature_correct and status_ok):
            error_message = f"Error in message: {feature_correct=}, {status_ok=}, {message=}"
            raise CommandError(error_message)
        message_channel_msb = message[CoinesPollingStreamResponse.SENSOR_ID_MSB.value]
        message_channel_lsb = message[CoinesPollingStreamResponse.SENSOR_ID_LSB.value]
        message_channel_id = (message_channel_msb << 8) | message_channel_lsb
        payload_start = CoinesPollingStreamResponse.DATA_START_POSITION.value
        payload_end = CoinesPollingStreamResponse.SENSOR_ID_MSB.value
        payload = message[payload_start:payload_end]
        payload_array = array("B", (int(el) for el in payload))
        return message_channel_id, payload_array
