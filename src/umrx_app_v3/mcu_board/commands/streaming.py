import logging
import struct
from array import array
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
class PollingStreamingSpiConfig:
    channel_configs: list[PollingStreamingSpiChannelConfig] = field(default_factory=list)


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
    polling_streaming_spi_config = PollingStreamingSpiConfig()

    @staticmethod
    def assemble(number_of_sensors: int, sampling_time: int, sampling_unit: StreamingSamplingUnit) -> array[int]:
        yield ConfigPollingStreamingCmd.set_sampling_time(
            number_of_sensors=number_of_sensors, sampling_time=sampling_time, sampling_unit=sampling_unit
        )

    @staticmethod
    def set_sampling_time(
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
    def set_streaming_channel_spi(
        cs_pin: MultiIOPin,
        sampling_time: int,
        sampling_unit: StreamingSamplingUnit,
        register_address: int,
        bytes_to_read: int,
    ) -> array[int]:
        channel_id = len(ConfigPollingStreamingCmd.polling_streaming_spi_config.channel_configs) + 1
        config = PollingStreamingSpiChannelConfig(
            id=channel_id,
            cs_pin=cs_pin,
            sampling_time=sampling_time,
            sampling_unit=sampling_unit,
            register_address=register_address,
            bytes_to_read=bytes_to_read,
        )
        ConfigPollingStreamingCmd.polling_streaming_spi_config.channel_configs.append(config)

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
