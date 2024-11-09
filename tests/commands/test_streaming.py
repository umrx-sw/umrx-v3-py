import logging
from array import array
from unittest.mock import patch

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, StreamingSamplingUnit
from umrx_app_v3.mcu_board.commands.command import Command, CommandError
from umrx_app_v3.mcu_board.commands.streaming import (
    ConfigPollingStreamingCmd,
    PollingStreamingI2cConfig,
    PollingStreamingSpiChannelConfig,
    PollingStreamingSpiConfig,
    StopInterruptStreamingCmd,
    StopPollingStreamingCmd,
)

logger = logging.getLogger(__name__)


@pytest.mark.commands
def test_command_stop_polling_streaming_assemble(stop_polling_streaming_command: StopPollingStreamingCmd) -> None:
    payload = stop_polling_streaming_command.assemble()

    assert payload == array("B", (0xAA, 0x06, 0x06, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_stop_polling_streaming_parse(stop_polling_streaming_command: StopPollingStreamingCmd) -> None:
    dummy_response = array("B", (0xCA, 0xFE))

    assert stop_polling_streaming_command.parse(dummy_response) is None


@pytest.mark.commands
def test_command_stop_interrupt_streaming_assemble(stop_interrupt_streaming_command: StopInterruptStreamingCmd) -> None:
    payload = stop_interrupt_streaming_command.assemble()

    assert payload == array("B", (0xAA, 0x06, 0x0A, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_stop_interrupt_streaming_parse(stop_interrupt_streaming_command: StopInterruptStreamingCmd) -> None:
    dummy_response = array("B", (0xCA, 0xFE))

    assert stop_interrupt_streaming_command.parse(dummy_response) is None


@pytest.mark.commands
def test_command_config_polling_streaming(config_polling_streaming_command: ConfigPollingStreamingCmd) -> None:
    payload = config_polling_streaming_command.set_sampling_time_direct(
        number_of_sensors=2, sampling_time=0x7D, sampling_unit=StreamingSamplingUnit.MICRO_SECOND
    )
    assert payload == array("B", (0xAA, 0x0A, 0x03, 0x02, 0x01, 0x00, 0x7D, 0x01, 0x0D, 0x0A))

    with pytest.raises(CommandError):
        config_polling_streaming_command.set_sampling_time_direct(
            number_of_sensors=5, sampling_time=0x7D, sampling_unit=StreamingSamplingUnit.MICRO_SECOND
        )


@pytest.mark.commands
def test_command_assemble_spi_channel_config(config_polling_streaming_command: ConfigPollingStreamingCmd) -> None:
    config = PollingStreamingSpiChannelConfig(
        id=1,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )
    payload = config_polling_streaming_command.assemble_spi_channel_config(config)

    expected_payload = array(
        "B",
        (
            0xAA,
            0x17,
            0x0F,
            0x01,
            0x00,
            0x16,
            0x01,
            0x00,
            0x00,
            0x02,
            0x71,
            0x01,
            0x01,
            0x01,
            0x12,
            0x00,
            0x07,
            0x00,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x0A,
        ),
    )

    assert payload == expected_payload

    config = PollingStreamingSpiChannelConfig(
        id=2,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )
    payload = config_polling_streaming_command.assemble_spi_channel_config(config)

    expected_payload = array(
        "B",
        (
            0xAA,
            0x17,
            0x0F,
            0x02,
            0x00,
            0x14,
            0x01,
            0x00,
            0x00,
            0x01,
            0xF4,
            0x01,
            0x01,
            0x01,
            0x02,
            0x00,
            0x06,
            0x00,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x0A,
        ),
    )

    assert payload == expected_payload


@pytest.mark.commands
def test_command_streaming_set_spi_config(config_polling_streaming_command: ConfigPollingStreamingCmd) -> None:
    config_polling_streaming_command.set_spi_config()
    assert isinstance(config_polling_streaming_command.polling_streaming_config, PollingStreamingSpiConfig)

    config_polling_streaming_command.polling_streaming_config = None


@pytest.mark.commands
def test_command_streaming_reset_spi_config(config_polling_streaming_command: ConfigPollingStreamingCmd) -> None:
    config = PollingStreamingSpiChannelConfig(
        id=1,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )
    config_polling_streaming_command.set_spi_config()
    config_polling_streaming_command.polling_streaming_config.channel_configs.append(config)
    assert len(config_polling_streaming_command.polling_streaming_config.channel_configs) == 1
    config_polling_streaming_command.reset_spi_config()
    assert len(config_polling_streaming_command.polling_streaming_config.channel_configs) == 0


@pytest.mark.commands
def test_command_streaming_configure_spi(config_polling_streaming_command: ConfigPollingStreamingCmd) -> None:
    config_polling_streaming_command.set_spi_config()

    config_polling_streaming_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )
    config_polling_streaming_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )
    with patch.object(Command, "create_message_from") as mocked_create:
        for _ in config_polling_streaming_command.configure_spi():
            ...

        assert mocked_create.call_count == 3


@pytest.mark.commands
def test_command_errors_in_set_sampling_time(config_polling_streaming_command: ConfigPollingStreamingCmd) -> None:
    config_polling_streaming_command.set_spi_config()
    config_polling_streaming_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )
    config_polling_streaming_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )
    config_polling_streaming_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_8,
        sampling_time=800,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x04,
        bytes_to_read=9,
    )
    with pytest.raises(CommandError):
        config_polling_streaming_command.set_sampling_time()

    config_polling_streaming_command.reset_spi_config()

    with pytest.raises(CommandError):
        config_polling_streaming_command.set_sampling_time()


@pytest.mark.commands
def test_command_one_sensor_set_sampling_time(config_polling_streaming_command: ConfigPollingStreamingCmd) -> None:
    config_polling_streaming_command.set_spi_config()
    config_polling_streaming_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )
    expected_payload = config_polling_streaming_command.set_sampling_time_direct(
        number_of_sensors=1, sampling_time=625, sampling_unit=StreamingSamplingUnit.MICRO_SECOND
    )

    payload = config_polling_streaming_command.set_sampling_time()

    assert payload == expected_payload


@pytest.mark.commands
def test_command_slow_sampling_time(config_polling_streaming_command: ConfigPollingStreamingCmd) -> None:
    config_polling_streaming_command.set_spi_config()
    config_polling_streaming_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        sampling_time=300,
        sampling_unit=StreamingSamplingUnit.MILLI_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )
    config_polling_streaming_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_8,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MILLI_SECOND,
        register_address=0x04,
        bytes_to_read=9,
    )
    expected_payload = config_polling_streaming_command.set_sampling_time_direct(
        number_of_sensors=2, sampling_time=100, sampling_unit=StreamingSamplingUnit.MILLI_SECOND
    )

    payload = config_polling_streaming_command.set_sampling_time()

    assert payload == expected_payload


@pytest.mark.commands
def test_command_streaming_set_reset_i2c_config(config_polling_streaming_command: ConfigPollingStreamingCmd) -> None:
    config_polling_streaming_command.set_i2c_config()
    assert isinstance(config_polling_streaming_command.polling_streaming_config, PollingStreamingI2cConfig)

    config_polling_streaming_command.reset_i2c_config()
    assert len(config_polling_streaming_command.polling_streaming_config.channel_configs) == 0
