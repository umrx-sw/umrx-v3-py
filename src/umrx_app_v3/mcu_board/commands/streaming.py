import logging
import struct
from array import array

from umrx_app_v3.mcu_board.bst_protocol_constants import CommandType, StreamingSamplingUnit
from umrx_app_v3.mcu_board.commands.command import Command, CommandError

logger = logging.getLogger(__name__)


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
    def parse(message: array[int]) -> None: ...
