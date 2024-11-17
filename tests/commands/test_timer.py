from array import array
from unittest.mock import patch

import pytest

from umrx_app_v3.mcu_board.commands.command import CommandError
from umrx_app_v3.mcu_board.commands.timer import TimerCmd


@pytest.mark.commands
def test_command_timer_disable(timer_command: TimerCmd) -> None:
    for idx, payload in enumerate(timer_command.disable()):
        if idx == 0:
            assert payload == array("B", (0xAA, 0x07, 0x01, 0x29, 0x00, 0x0D, 0x0A))
        elif idx == 1:
            assert payload == array("B", (0xAA, 0x07, 0x02, 0x29, 0x04, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_timer_enable(timer_command: TimerCmd) -> None:
    for idx, payload in enumerate(timer_command.enable()):
        if idx == 0:
            assert payload == array("B", (0xAA, 0x07, 0x01, 0x29, 0x01, 0x0D, 0x0A))
        elif idx == 1:
            assert payload == array("B", (0xAA, 0x07, 0x02, 0x29, 0x03, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_timer_assemble(timer_command: TimerCmd) -> None:
    with patch.object(TimerCmd, "enable") as mocked_enable, patch.object(TimerCmd, "disable") as mocked_disable:
        timer_command.assemble(switch="on")
        mocked_enable.assert_called_once()
        mocked_disable.assert_not_called()

    with patch.object(TimerCmd, "enable") as mocked_enable, patch.object(TimerCmd, "disable") as mocked_disable:
        timer_command.assemble(switch="off")
        mocked_disable.assert_called_once()
        mocked_enable.assert_not_called()

    with pytest.raises(CommandError):
        timer_command.assemble(switch="unsupported")


@pytest.mark.commands
def test_command_timer_parse(timer_command: TimerCmd) -> None:
    dummy_messsage = array("B", (0xCA, 0xFE))
    assert timer_command.parse(dummy_messsage) is None
