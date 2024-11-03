import struct
import logging
from array import array
from umrx_app_v3.mcu_board.commands.command import Command
from umrx_app_v3.mcu_board.bst_protocol_constants import CommandType, CommandId


logger = logging.getLogger(__name__)

Volts = float


class SetVddVddioCmd(Command):

    @staticmethod
    def assemble(vdd: Volts, vddio: Volts):
        is_vdd_nonzero = vdd != 0
        is_vddio_nonzero = vddio != 0
        payload = (CommandType.DD_SET.value, CommandId.SHUTTLE_BOARD_VDD_VDDIO_CONFIGURATION.value,
                   *SetVddVddioCmd.voltage_to_payload(vdd),
                   is_vdd_nonzero, *SetVddVddioCmd.voltage_to_payload(vddio), is_vddio_nonzero)
        return Command.create_message_from(payload)

    @staticmethod
    def voltage_to_payload(voltage: Volts) -> tuple[int, ...]:
        voltage_milli_volt = int(voltage * 1000)
        return tuple(int(el) for el in struct.pack(">H", voltage_milli_volt))

    @staticmethod
    def parse(message: array[int]): ...
