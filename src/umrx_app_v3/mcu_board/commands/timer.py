import logging
from array import array
from umrx_app_v3.mcu_board.commands.command import Command
from umrx_app_v3.mcu_board.bst_protocol_constants import CommandType, CommandId, TimerStampConfig


logger = logging.getLogger(__name__)


class StopTimerCmd(Command):
    @staticmethod
    def assemble():
        payload = (CommandType.DD_SET.value, CommandId.TIMER_CFG_CMD_ID.value, TimerStampConfig.TIMESTAMP_DISABLE.value)
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]): ...
