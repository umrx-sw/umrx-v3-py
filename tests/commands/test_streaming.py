from array import array

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import StreamingSamplingUnit, StreamingMode
from umrx_app_v3.mcu_board.commands.command import CommandError
from umrx_app_v3.mcu_board.commands.streaming import (StopInterruptStreamingCmd, StopPollingStreamingCmd,
                                                      ConfigPollingStreamingCmd)


@pytest.mark.commands
def test_command_stop_polling_streaming_assemble(stop_polling_streaming_command: StopPollingStreamingCmd) -> None:
    payload = stop_polling_streaming_command.assemble()

    assert payload == array("B", (0xAA, 0x06, 0x06, 0x00, 0x0D, 0x0A,))


@pytest.mark.commands
def test_command_stop_polling_streaming_parse(stop_polling_streaming_command: StopPollingStreamingCmd) -> None:
    dummy_response = array('B', (0xCA, 0xFE))

    assert stop_polling_streaming_command.parse(dummy_response) is None


@pytest.mark.commands
def test_command_stop_interrupt_streaming_assemble(stop_interrupt_streaming_command: StopInterruptStreamingCmd) -> None:
    payload = stop_interrupt_streaming_command.assemble()

    assert payload == array("B", (0xAA, 0x06, 0x0A, 0x00, 0x0D, 0x0A,))


@pytest.mark.commands
def test_command_stop_interrupt_streaming_parse(stop_interrupt_streaming_command: StopInterruptStreamingCmd) -> None:
    dummy_response = array('B', (0xCA, 0xFE))

    assert stop_interrupt_streaming_command.parse(dummy_response) is None


@pytest.mark.commands
def test_command_config_polling_streaming(config_polling_streaming_command: ConfigPollingStreamingCmd) -> None:
    payload = config_polling_streaming_command.assemble(
        number_of_sensors=2, sampling_time=0x7D, sampling_unit=StreamingSamplingUnit.MICRO_SECOND
    )
    assert payload == array("B", (0xAA, 0x0A, 0x03, 0x02, 0x01, 0x00, 0x7D, 0x01, 0x0D, 0x0A,))

    with pytest.raises(CommandError):
        config_polling_streaming_command.assemble(
            number_of_sensors=5, sampling_time=0x7D, sampling_unit=StreamingSamplingUnit.MICRO_SECOND
        )
