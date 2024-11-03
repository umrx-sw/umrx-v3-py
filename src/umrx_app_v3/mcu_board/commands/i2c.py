import logging
from array import array

from umrx_app_v3.mcu_board.bst_protocol_constants import CommandId, CommandType, InterfaceSDO, SensorInterface
from umrx_app_v3.mcu_board.commands.command import Command

logger = logging.getLogger(__name__)


class I2CConfigureCmd(Command):
    @staticmethod
    def assemble() -> array[int]:
        payload = (
            CommandType.DD_SET.value,
            CommandId.INTERFACE.value,
            SensorInterface.I2C.value,
            InterfaceSDO.SDO_LOW.value,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> None: ...
