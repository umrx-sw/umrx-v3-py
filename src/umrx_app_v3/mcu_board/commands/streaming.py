import logging
from array import array
from umrx_app_v3.mcu_board.commands.command import Command
from umrx_app_v3.mcu_board.bst_protocol_constants import CommandType


logger = logging.getLogger(__name__)


class StopPollingStreamingCmd(Command):
    @staticmethod
    def assemble():
        num_samples = 0
        payload = (CommandType.DD_START_STOP_STREAMING_POLLING.value, num_samples)
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]): ...


class StopInterruptStreamingCmd(Command):
    @staticmethod
    def assemble():
        num_samples = 0
        payload = (CommandType.DD_START_STOP_STREAMING_INTERRUPT.value, num_samples)
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]): ...
