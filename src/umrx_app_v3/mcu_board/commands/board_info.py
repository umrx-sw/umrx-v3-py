from array import array
from dataclasses import dataclass

from umrx_app_v3.mcu_board.bst_protocol_constants import CommandId, CommandType
from umrx_app_v3.mcu_board.commands.command import Command


@dataclass
class BoardInfo:
    board_id: int
    hardware_id: int
    software_id: int
    shuttle_id: int


class BoardInfoCmd(Command):
    @staticmethod
    def assemble() -> array[int]:
        payload = CommandType.DD_GET.value, CommandId.BOARD_INFORMATION.value
        return Command.create_message_from(payload)

    @staticmethod
    @Command.check_message_length(expected=15)
    def parse(message: array[int]) -> BoardInfo:
        shuttle_id = message[6] << 8 | message[7]
        hardware_id = message[8] << 8 | message[9]
        software_id = message[10] << 8 | message[11]
        board_id = message[12]
        return BoardInfo(board_id=board_id, hardware_id=hardware_id, software_id=software_id, shuttle_id=shuttle_id)
