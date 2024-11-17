import logging
from array import array
from collections.abc import Generator
from typing import Literal

from umrx_app_v3.mcu_board.bst_protocol_constants import CommandId, CommandType, TimerConfig
from umrx_app_v3.mcu_board.commands.command import Command, CommandError

logger = logging.getLogger(__name__)


class TimerCmd(Command):
    @staticmethod
    def assemble(switch: Literal["on", "off"]) -> Generator:
        if switch == "on":
            return TimerCmd.enable()
        if switch == "off":
            return TimerCmd.disable()
        error_message = f"Timer switch can be 'on' / 'off', provided: {switch}"
        raise CommandError(error_message)

    @staticmethod
    def _start() -> array[int]:
        payload = (CommandType.DD_SET.value, CommandId.TIMER_CFG_CMD_ID.value, TimerConfig.START.value)
        return Command.create_message_from(payload)

    @staticmethod
    def _stop() -> array[int]:
        payload = (CommandType.DD_SET.value, CommandId.TIMER_CFG_CMD_ID.value, TimerConfig.STOP.value)
        return Command.create_message_from(payload)

    @staticmethod
    def _enable() -> array[int]:
        payload = (CommandType.DD_GET.value, CommandId.TIMER_CFG_CMD_ID.value, TimerConfig.ENABLE.value)
        return Command.create_message_from(payload)

    @staticmethod
    def _disable() -> array[int]:
        payload = (CommandType.DD_GET.value, CommandId.TIMER_CFG_CMD_ID.value, TimerConfig.DISABLE.value)
        return Command.create_message_from(payload)

    @staticmethod
    def disable() -> Generator:
        yield TimerCmd._stop()
        yield TimerCmd._disable()

    @staticmethod
    def enable() -> Generator:
        yield TimerCmd._start()
        yield TimerCmd._enable()

    @staticmethod
    def parse(message: array[int]) -> None: ...
