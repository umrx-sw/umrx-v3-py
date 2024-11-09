from array import array

import pytest

from umrx_app_v3.mcu_board.commands.streaming_interrupt import StopInterruptStreamingCmd


@pytest.mark.commands
def test_command_stop_interrupt_streaming_assemble(stop_interrupt_streaming_command: StopInterruptStreamingCmd) -> None:
    payload = stop_interrupt_streaming_command.assemble()

    assert payload == array("B", (0xAA, 0x06, 0x0A, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_stop_interrupt_streaming_parse(stop_interrupt_streaming_command: StopInterruptStreamingCmd) -> None:
    dummy_response = array("B", (0xCA, 0xFE))

    assert stop_interrupt_streaming_command.parse(dummy_response) is None
