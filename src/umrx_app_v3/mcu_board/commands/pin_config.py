import logging
from array import array

from umrx_app_v3.mcu_board.bst_protocol_constants import CommandId, CommandType, MultiIOPin, PinDirection, PinValue
from umrx_app_v3.mcu_board.commands.command import Command, CommandError

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


class GetPinConfigCmd(Command):
    @staticmethod
    def assemble(pin: MultiIOPin) -> array[int]:
        coines_mini_shuttle_pin = 1 << 7
        payload = (
            CommandType.DD_GET.value,
            CommandId.MULTIO_CONFIGURATION.value,
            coines_mini_shuttle_pin,
            pin.value,
        )
        return Command.create_message_from(payload)

    @staticmethod
    def parse(message: array[int]) -> tuple[PinDirection, PinValue]:
        ok = Command.check_message(message)
        if not ok:
            error_message = "Invalid message to parse"
            raise CommandError(error_message)
        pin_direction = message[8] << 8 | message[9]
        pin_value = message[10] << 8 | message[11]
        return PinDirection(pin_direction), PinValue(pin_value)
