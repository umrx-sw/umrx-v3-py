import logging
import math
import struct
from array import array
from collections.abc import Generator
from dataclasses import dataclass, field

from umrx_app_v3.mcu_board.bst_protocol_constants import CommandType, MultiIOPin, StreamingSamplingUnit
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


class StopPollingStreamingCmd(Command):
    @staticmethod
    def assemble() -> array[int]:
        num_samples = 0
        payload = (CommandType.DD_START_STOP_STREAMING_POLLING.value, num_samples)
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> None: ...


class StopInterruptStreamingCmd(Command):
    @staticmethod
    def assemble() -> array[int]:
        num_samples = 0
        payload = (CommandType.DD_START_STOP_STREAMING_INTERRUPT.value, num_samples)
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> None: ...


class ConfigPollingStreamingCmd(Command):
    polling_streaming_config: PollingStreamingSpiConfig | PollingStreamingI2cConfig | None = None

    @staticmethod
    def set_spi_config() -> None:
        ConfigPollingStreamingCmd.polling_streaming_config = PollingStreamingSpiConfig()

    @staticmethod
    def reset_spi_config() -> None:
        ConfigPollingStreamingCmd.set_spi_config()

    @staticmethod
    def set_i2c_config() -> None:
        ConfigPollingStreamingCmd.polling_streaming_config = PollingStreamingI2cConfig()

    @staticmethod
    def reset_i2c_config() -> None:
        ConfigPollingStreamingCmd.set_i2c_config()

    @staticmethod
    def assemble() -> None: ...

    @staticmethod
    def configure_spi() -> Generator:
        yield ConfigPollingStreamingCmd.set_sampling_time()
        for config in ConfigPollingStreamingCmd.polling_streaming_config.channel_configs:
            yield ConfigPollingStreamingCmd.assemble_spi_channel_config(config)

    @staticmethod
    def configure_i2c() -> Generator: ...

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
        number_of_sensors = len(ConfigPollingStreamingCmd.polling_streaming_config.channel_configs)
        if number_of_sensors > 2:
            message = f"Exceeds max supported number of sensors = 2, attempted: {number_of_sensors}"
            raise CommandError(message)

        if number_of_sensors == 2:
            streaming_time_1 = ConfigPollingStreamingCmd.polling_streaming_config.channel_configs[0].sampling_time
            streaming_unit_1 = ConfigPollingStreamingCmd.polling_streaming_config.channel_configs[0].sampling_unit

            streaming_time_2 = ConfigPollingStreamingCmd.polling_streaming_config.channel_configs[1].sampling_time
            streaming_unit_2 = ConfigPollingStreamingCmd.polling_streaming_config.channel_configs[1].sampling_unit

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
            sampling_time = ConfigPollingStreamingCmd.polling_streaming_config.channel_configs[0].sampling_time
            sampling_unit = ConfigPollingStreamingCmd.polling_streaming_config.channel_configs[0].sampling_unit
        else:
            error_msg = "Specify streaming configuration first, call set_streaming_channel_[i2c|spi] before!"
            raise CommandError(error_msg)
        return ConfigPollingStreamingCmd.set_sampling_time_direct(
            number_of_sensors=number_of_sensors, sampling_time=sampling_time, sampling_unit=sampling_unit
        )

    @staticmethod
    def set_streaming_channel_spi(
        cs_pin: MultiIOPin,
        sampling_time: int,
        sampling_unit: StreamingSamplingUnit,
        register_address: int,
        bytes_to_read: int,
    ) -> array[int]:
        channel_id = len(ConfigPollingStreamingCmd.polling_streaming_config.channel_configs) + 1
        config = PollingStreamingSpiChannelConfig(
            id=channel_id,
            cs_pin=cs_pin,
            sampling_time=sampling_time,
            sampling_unit=sampling_unit,
            register_address=register_address,
            bytes_to_read=bytes_to_read,
        )
        ConfigPollingStreamingCmd.polling_streaming_config.channel_configs.append(config)

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
    def set_streaming_channel_i2c() -> None: ...

    @staticmethod
    def parse(message: array[int]) -> None: ...
