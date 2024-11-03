import logging
from array import array

from umrx_app_v3.mcu_board.bst_protocol_constants import CommandId, CommandType, TimerStampConfig
from umrx_app_v3.mcu_board.commands.command import Command

logger = logging.getLogger(__name__)


class StopTimerCmd(Command):
    @staticmethod
    def assemble() -> array[int]:
        payload = (CommandType.DD_SET.value, CommandId.TIMER_CFG_CMD_ID.value, TimerStampConfig.TIMESTAMP_DISABLE.value)
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> None: ...
