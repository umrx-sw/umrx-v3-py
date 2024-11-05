import logging
from array import array

from umrx_app_v3.mcu_board.bst_protocol_constants import CommandId, CommandType, MultiIOPin, PinDirection, PinValue
from umrx_app_v3.mcu_board.commands.command import Command

logger = logging.getLogger(__name__)


class SetPinConfigCmd(Command):
    @staticmethod
    def assemble(pin: MultiIOPin, direction: PinDirection, value: PinValue) -> array[int]:
        coines_mini_shuttle_pin = 1 << 7
        payload = (
            CommandType.DD_SET.value,
            CommandId.MULTIO_CONFIGURATION.value,
            coines_mini_shuttle_pin,
            pin.value,
            0,
            direction.value,
            0,
            value.value,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> None: ...
