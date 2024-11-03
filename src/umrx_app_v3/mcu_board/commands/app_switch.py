import logging
import struct
from array import array

from umrx_app_v3.mcu_board.bst_protocol_constants import CommandId, CommandType
from umrx_app_v3.mcu_board.commands.command import Command

logger = logging.getLogger(__name__)


class AppSwitchCmd(Command):
    @staticmethod
    def assemble(address: int = 0) -> array[int]:
        address_serialized = (int(a) for a in struct.pack(">L", address))
        payload = (CommandType.DD_SET.value, CommandId.APP_SWITCH.value, *address_serialized)
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> None: ...
