import logging
from array import array
from unittest.mock import patch

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, StreamingSamplingUnit
from umrx_app_v3.mcu_board.commands.command import Command, CommandError
from umrx_app_v3.mcu_board.commands.streaming_polling import (
    PollingStreamingI2cChannelConfig,
    PollingStreamingI2cConfig,
    PollingStreamingSpiChannelConfig,
    PollingStreamingSpiConfig,
    StreamingPollingCmd,
)

logger = logging.getLogger(__name__)


@pytest.mark.commands
def test_polling_streaming_stop(streaming_polling_command: StreamingPollingCmd) -> None:
    payload = streaming_polling_command.stop_streaming()

    assert payload == array("B", (0xAA, 0x06, 0x06, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_polling_streaming_set_time_direct(streaming_polling_command: StreamingPollingCmd) -> None:
    payload = streaming_polling_command.set_sampling_time_direct(
        number_of_sensors=2, sampling_time=0x7D, sampling_unit=StreamingSamplingUnit.MICRO_SECOND
    )
    assert payload == array("B", (0xAA, 0x0A, 0x03, 0x02, 0x01, 0x00, 0x7D, 0x01, 0x0D, 0x0A))

    with pytest.raises(CommandError):
        streaming_polling_command.set_sampling_time_direct(
            number_of_sensors=5, sampling_time=0x7D, sampling_unit=StreamingSamplingUnit.MICRO_SECOND
        )


@pytest.mark.commands
def test_polling_assemble_spi_channel_config(streaming_polling_command: StreamingPollingCmd) -> None:
    config = PollingStreamingSpiChannelConfig(
        id=1,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )
    payload = streaming_polling_command.assemble_spi_channel_config(config)

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
    payload = streaming_polling_command.assemble_spi_channel_config(config)

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
def test_polling_streaming_set_spi_config(streaming_polling_command: StreamingPollingCmd) -> None:
    streaming_polling_command.set_spi_config()
    assert isinstance(streaming_polling_command.polling_streaming_config, PollingStreamingSpiConfig)

    streaming_polling_command.polling_streaming_config = None


@pytest.mark.commands
def test_polling_streaming_reset_spi_config(streaming_polling_command: StreamingPollingCmd) -> None:
    config = PollingStreamingSpiChannelConfig(
        id=1,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )
    streaming_polling_command.set_spi_config()
    streaming_polling_command.polling_streaming_config.channel_configs.append(config)
    assert len(streaming_polling_command.polling_streaming_config.channel_configs) == 1
    streaming_polling_command.reset_spi_config()
    assert len(streaming_polling_command.polling_streaming_config.channel_configs) == 0


@pytest.mark.commands
def test_polling_streaming_configure_spi(streaming_polling_command: StreamingPollingCmd) -> None:
    streaming_polling_command.set_spi_config()

    streaming_polling_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )
    streaming_polling_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )
    with patch.object(Command, "create_message_from") as mocked_create:
        for _ in streaming_polling_command.configure_spi():
            ...

        assert mocked_create.call_count == 3


@pytest.mark.commands
def test_polling_errors_in_set_sampling_time(streaming_polling_command: StreamingPollingCmd) -> None:
    streaming_polling_command.set_spi_config()
    streaming_polling_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )
    streaming_polling_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )
    streaming_polling_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_8,
        sampling_time=800,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x04,
        bytes_to_read=9,
    )
    with pytest.raises(CommandError):
        streaming_polling_command.set_sampling_time()

    streaming_polling_command.reset_spi_config()

    with pytest.raises(CommandError):
        streaming_polling_command.set_sampling_time()


@pytest.mark.commands
def test_polling_one_sensor_set_sampling_time(streaming_polling_command: StreamingPollingCmd) -> None:
    streaming_polling_command.set_spi_config()
    streaming_polling_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )
    expected_payload = streaming_polling_command.set_sampling_time_direct(
        number_of_sensors=1, sampling_time=625, sampling_unit=StreamingSamplingUnit.MICRO_SECOND
    )

    payload = streaming_polling_command.set_sampling_time()

    assert payload == expected_payload


@pytest.mark.commands
def test_polling_slow_sampling_time(streaming_polling_command: StreamingPollingCmd) -> None:
    streaming_polling_command.set_spi_config()
    streaming_polling_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        sampling_time=300,
        sampling_unit=StreamingSamplingUnit.MILLI_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )
    streaming_polling_command.set_streaming_channel_spi(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_8,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MILLI_SECOND,
        register_address=0x04,
        bytes_to_read=9,
    )
    expected_payload = streaming_polling_command.set_sampling_time_direct(
        number_of_sensors=2, sampling_time=100, sampling_unit=StreamingSamplingUnit.MILLI_SECOND
    )

    payload = streaming_polling_command.set_sampling_time()

    assert payload == expected_payload


@pytest.mark.commands
def test_polling_streaming_set_reset_i2c_config(streaming_polling_command: StreamingPollingCmd) -> None:
    streaming_polling_command.set_i2c_config()
    assert isinstance(streaming_polling_command.polling_streaming_config, PollingStreamingI2cConfig)

    streaming_polling_command.reset_i2c_config()
    assert len(streaming_polling_command.polling_streaming_config.channel_configs) == 0


@pytest.mark.commands
def test_polling_streaming_i2c_configure_channel(streaming_polling_command: StreamingPollingCmd) -> None:
    streaming_polling_command.set_i2c_config()

    config_1 = PollingStreamingI2cChannelConfig(
        id=1,
        i2c_address=0x18,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=6,
    )
    payload = streaming_polling_command.assemble_i2c_channel_config(config_1)

    expected_payload = array(
        "B",
        (
            0xAA,
            0x17,
            0x0F,
            0x01,
            0x00,
            0x00,
            0x01,
            0x00,
            0x18,
            0x02,
            0x71,
            0x01,
            0x01,
            0x01,
            0x12,
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

    config_2 = PollingStreamingI2cChannelConfig(
        id=2,
        i2c_address=0x68,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )
    payload = streaming_polling_command.assemble_i2c_channel_config(config_2)

    expected_payload = array(
        "B",
        (
            0xAA,
            0x17,
            0x0F,
            0x02,
            0x00,
            0x00,
            0x01,
            0x00,
            0x68,
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
def test_polling_streaming_i2c_set_channel(streaming_polling_command: StreamingPollingCmd) -> None:
    streaming_polling_command.set_i2c_config()

    config_1 = PollingStreamingI2cChannelConfig(
        id=1,
        i2c_address=0x18,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=6,
    )

    streaming_polling_command.set_streaming_channel_i2c(
        i2c_address=0x18,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=6,
    )

    saved_config = streaming_polling_command.polling_streaming_config.channel_configs[0]

    assert saved_config == config_1


@pytest.mark.commands
def test_polling_streaming_configure_i2c(streaming_polling_command: StreamingPollingCmd) -> None:
    streaming_polling_command.set_i2c_config()

    streaming_polling_command.set_streaming_channel_i2c(
        i2c_address=0x18,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=6,
    )

    streaming_polling_command.set_streaming_channel_i2c(
        i2c_address=0x68,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )

    with patch.object(Command, "create_message_from") as mocked_create:
        for _ in streaming_polling_command.configure_i2c():
            ...
        assert mocked_create.call_count == 3


@pytest.mark.commands
def test_polling_streaming_start(streaming_polling_command: StreamingPollingCmd) -> None:
    payload = streaming_polling_command.start_streaming()

    expected_payload = array("B", (0xAA, 0x06, 0x06, 0xFF, 0x0D, 0x0A))

    assert payload == expected_payload


@pytest.mark.commands
def test_polling_streaming_parse(streaming_polling_command: StreamingPollingCmd) -> None:
    streaming_packet = array(
        "B", (0xAA, 0x0F, 0x01, 0x00, 0x87, 0x7C, 0x00, 0xC1, 0x00, 0x4B, 0x15, 0x00, 0x01, 0x0D, 0x0A)
    )
    expected_payload = array("B", (0x7C, 0x00, 0xC1, 0x00, 0x4B, 0x15))
    sensor_id, payload = streaming_polling_command.parse(streaming_packet)
    assert sensor_id == 1
    assert len(payload) == 6
    assert payload == expected_payload

    streaming_packet = array(
        "B", (0xAA, 0x0F, 0x01, 0x00, 0x87, 0x06, 0x00, 0xCB, 0xFF, 0x24, 0x00, 0x00, 0x02, 0x0D, 0x0A)
    )
    expected_payload = array("B", (0x06, 0x00, 0xCB, 0xFF, 0x24, 0x00))
    sensor_id, payload = streaming_polling_command.parse(streaming_packet)
    assert sensor_id == 2
    assert len(payload) == 6
    assert payload == expected_payload


@pytest.mark.commands
def test_polling_streaming_parse_errors(streaming_polling_command: StreamingPollingCmd) -> None:
    invalid_packet = array(
        "B", (0xAA, 0xBB, 0x01, 0x00, 0x87, 0x06, 0x00, 0xCB, 0xFF, 0x24, 0x00, 0x00, 0x02, 0xCA, 0xFE)
    )
    with pytest.raises(CommandError):
        streaming_polling_command.parse(invalid_packet)

    invalid_status = array(
        "B", (0xAA, 0x0F, 0x01, 0x04, 0x87, 0x06, 0x00, 0xCB, 0xFF, 0x24, 0x00, 0x00, 0x02, 0x0D, 0x0A)
    )

    with pytest.raises(CommandError):
        streaming_polling_command.parse(invalid_status)

    invalid_feature = array(
        "B", (0xAA, 0x0F, 0x01, 0x04, 0x87, 0x06, 0x00, 0xCB, 0xFF, 0x24, 0x00, 0x00, 0x02, 0x0D, 0x0A)
    )

    with pytest.raises(CommandError):
        streaming_polling_command.parse(invalid_feature)
