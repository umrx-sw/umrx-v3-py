import logging
from array import array

import pytest

from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin
from umrx_app_v3.mcu_board.commands.command import CommandError
from umrx_app_v3.mcu_board.commands.streaming_interrupt import (
    StreamingInterruptCmd,
    StreamingInterruptI2cChannelConfig,
    StreamingInterruptI2cConfig,
    StreamingInterruptSpiChannelConfig,
    StreamingInterruptSpiConfig,
)

logger = logging.getLogger(__name__)


@pytest.mark.commands
def test_command_stop_interrupt_streaming_assemble(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    payload = streaming_interrupt_command.stop_streaming()

    assert payload == array("B", (0xAA, 0x06, 0x0A, 0x00, 0x0D, 0x0A))


@pytest.mark.commands
def test_command_interrupt_assemble_spi_channel_config(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    config_1 = StreamingInterruptSpiChannelConfig(
        id=1,
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        register_address=0x12,
        bytes_to_read=7,
    )
    expected_payload = array(
        "B",
        (
            0xAA,
            0x17,
            0x0E,
            0x01,
            0x01,
            0x16,
            0x12,
            0x00,
            0x00,
            0x01,
            0x01,
            0x12,
            0x00,
            0x07,
            0xF0,
            0xF0,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x0A,
        ),
    )
    payload = streaming_interrupt_command.assemble_spi_channel_config(config_1)
    assert payload == expected_payload

    config_2 = StreamingInterruptSpiChannelConfig(
        id=2,
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_7,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        register_address=0x02,
        bytes_to_read=6,
    )
    expected_payload = array(
        "B",
        (
            0xAA,
            0x17,
            0x0E,
            0x02,
            0x01,
            0x14,
            0x13,
            0x00,
            0x00,
            0x01,
            0x01,
            0x02,
            0x00,
            0x06,
            0xF0,
            0xF0,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x0A,
        ),
    )

    payload = streaming_interrupt_command.assemble_spi_channel_config(config_2)

    assert payload == expected_payload


@pytest.mark.commands
def test_command_interrupt_set_spi_channel_config(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    config_1 = StreamingInterruptSpiChannelConfig(
        id=1,
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        register_address=0x12,
        bytes_to_read=7,
    )

    streaming_interrupt_command.set_spi_config()

    streaming_interrupt_command.set_streaming_channel_spi(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        register_address=0x12,
        bytes_to_read=7,
    )
    assert len(streaming_interrupt_command.streaming_interrupt_config.channel_configs) == 1

    assert streaming_interrupt_command.streaming_interrupt_config.channel_configs[0] == config_1


@pytest.mark.commands
def test_command_interrupt_assemble_i2c_channel_config(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    config_1 = StreamingInterruptI2cChannelConfig(
        id=1, interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6, i2c_address=0x18, register_address=0x12, bytes_to_read=6
    )
    expected_payload = array(
        "B",
        (
            0xAA,
            0x17,
            0x0E,
            0x01,
            0x01,
            0x00,
            0x12,
            0x00,
            0x18,
            0x01,
            0x01,
            0x12,
            0x00,
            0x06,
            0xF0,
            0xF0,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x0A,
        ),
    )

    payload = streaming_interrupt_command.assemble_i2c_channel_config(config_1)
    assert payload == expected_payload

    config_2 = StreamingInterruptI2cChannelConfig(
        id=2, interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_7, i2c_address=0x68, register_address=0x02, bytes_to_read=6
    )
    expected_payload = array(
        "B",
        (
            0xAA,
            0x17,
            0x0E,
            0x02,
            0x01,
            0x00,
            0x13,
            0x00,
            0x68,
            0x01,
            0x01,
            0x02,
            0x00,
            0x06,
            0xF0,
            0xF0,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x0A,
        ),
    )

    payload = streaming_interrupt_command.assemble_i2c_channel_config(config_2)

    assert payload == expected_payload


@pytest.mark.commands
def test_command_interrupt_set_i2c_channel_config(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    config_1 = StreamingInterruptI2cChannelConfig(
        id=1, interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6, i2c_address=0x18, register_address=0x12, bytes_to_read=6
    )

    streaming_interrupt_command.set_i2c_config()

    streaming_interrupt_command.set_streaming_channel_i2c(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6, i2c_address=0x18, register_address=0x12, bytes_to_read=6
    )
    assert len(streaming_interrupt_command.streaming_interrupt_config.channel_configs) == 1

    assert streaming_interrupt_command.streaming_interrupt_config.channel_configs[0] == config_1


@pytest.mark.commands
def test_command_interrupt_configure_i2c(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    streaming_interrupt_command.set_i2c_config()
    streaming_interrupt_command.set_streaming_channel_i2c(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6, i2c_address=0x18, register_address=0x12, bytes_to_read=6
    )
    streaming_interrupt_command.set_streaming_channel_i2c(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_7, i2c_address=0x68, register_address=0x02, bytes_to_read=6
    )
    expected_payload_1 = array(
        "B",
        (
            0xAA,
            0x17,
            0x0E,
            0x01,
            0x01,
            0x00,
            0x12,
            0x00,
            0x18,
            0x01,
            0x01,
            0x12,
            0x00,
            0x06,
            0xF0,
            0xF0,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x0A,
        ),
    )

    expected_payload_2 = array(
        "B",
        (
            0xAA,
            0x17,
            0x0E,
            0x02,
            0x01,
            0x00,
            0x13,
            0x00,
            0x68,
            0x01,
            0x01,
            0x02,
            0x00,
            0x06,
            0xF0,
            0xF0,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x0A,
        ),
    )
    for idx, payload in enumerate(streaming_interrupt_command.configure_i2c()):
        if idx == 0:
            assert payload == expected_payload_1
        if idx == 1:
            assert payload == expected_payload_2


@pytest.mark.commands
def test_command_interrupt_configure_spi(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    streaming_interrupt_command.set_spi_config()
    streaming_interrupt_command.set_streaming_channel_spi(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        register_address=0x12,
        bytes_to_read=7,
    )
    streaming_interrupt_command.set_streaming_channel_spi(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_7,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        register_address=0x02,
        bytes_to_read=6,
    )
    expected_payload_1 = array(
        "B",
        (
            0xAA,
            0x17,
            0x0E,
            0x01,
            0x01,
            0x16,
            0x12,
            0x00,
            0x00,
            0x01,
            0x01,
            0x12,
            0x00,
            0x07,
            0xF0,
            0xF0,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x0A,
        ),
    )

    expected_payload_2 = array(
        "B",
        (
            0xAA,
            0x17,
            0x0E,
            0x02,
            0x01,
            0x14,
            0x13,
            0x00,
            0x00,
            0x01,
            0x01,
            0x02,
            0x00,
            0x06,
            0xF0,
            0xF0,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x0A,
        ),
    )
    for idx, payload in enumerate(streaming_interrupt_command.configure_spi()):
        if idx == 0:
            assert payload == expected_payload_1
        if idx == 1:
            assert payload == expected_payload_2


@pytest.mark.commands
def test_command_interrupt_start(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    expected_response = array("B", (0xAA, 0x06, 0x0A, 0xFF, 0x0D, 0x0A))

    assert streaming_interrupt_command.start_streaming() == expected_response


@pytest.mark.commands
def test_command_interrupt_reset_i2c_config(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    streaming_interrupt_command.reset_i2c_config()

    assert isinstance(streaming_interrupt_command.streaming_interrupt_config, StreamingInterruptI2cConfig)
    assert len(streaming_interrupt_command.streaming_interrupt_config.channel_configs) == 0


@pytest.mark.commands
def test_command_interrupt_reset_spi_config(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    streaming_interrupt_command.reset_spi_config()

    assert isinstance(streaming_interrupt_command.streaming_interrupt_config, StreamingInterruptSpiConfig)
    assert len(streaming_interrupt_command.streaming_interrupt_config.channel_configs) == 0


@pytest.mark.commands
def test_command_interrupt_assemble(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    streaming_interrupt_command.set_i2c_config()
    streaming_interrupt_command.set_streaming_channel_i2c(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6, i2c_address=0x18, register_address=0x12, bytes_to_read=6
    )
    streaming_interrupt_command.set_streaming_channel_i2c(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_7, i2c_address=0x68, register_address=0x02, bytes_to_read=6
    )
    for payload in streaming_interrupt_command.assemble(sensor_interface="i2c"):
        logger.info(f"{payload=}")

    streaming_interrupt_command.set_spi_config()

    streaming_interrupt_command.set_streaming_channel_spi(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        register_address=0x12,
        bytes_to_read=7,
    )
    streaming_interrupt_command.set_streaming_channel_spi(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_7,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        register_address=0x02,
        bytes_to_read=6,
    )
    for payload in streaming_interrupt_command.assemble(sensor_interface="spi"):
        logger.info(f"{payload=}")

    with pytest.raises(CommandError):
        streaming_interrupt_command.assemble(sensor_interface="pci")


@pytest.mark.commands
def test_command_interrupt_streaming_parse(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    response = array("B", [170, 18, 1, 0, 138, 1, 0, 0, 0, 49, 168, 0, 69, 0, 77, 21, 13, 10])

    channel_id, packet_idx, timestamp, payload = streaming_interrupt_command.parse(response)
    assert channel_id == 1
    assert packet_idx == 49
    assert timestamp == -1
    assert payload == array("B", [168, 0, 69, 0, 77, 21])


@pytest.mark.commands
def test_command_interrupt_streaming_parse_invalid(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    invalid_response = array("B", [170, 22, 1, 0, 138, 1, 0, 0, 0, 49, 168, 0, 69, 0, 77, 21])

    with pytest.raises(CommandError):
        _ = streaming_interrupt_command.parse(invalid_response)

    status_error = array("B", [170, 18, 1, 22, 138, 1, 0, 0, 0, 49, 168, 0, 69, 0, 77, 21, 13, 10])
    with pytest.raises(CommandError):
        _ = streaming_interrupt_command.parse(status_error)

    feature_invalid = array("B", [170, 18, 1, 0, 135, 1, 0, 0, 0, 49, 168, 0, 69, 0, 77, 21, 13, 10])
    with pytest.raises(CommandError):
        _ = streaming_interrupt_command.parse(feature_invalid)

    both_invalid = array("B", [170, 18, 1, 22, 135, 1, 0, 0, 0, 49, 168, 0, 69, 0, 77, 21, 13, 10])
    with pytest.raises(CommandError):
        _ = streaming_interrupt_command.parse(both_invalid)


@pytest.mark.commands
def test_command_interrupt_streaming_parse_with_timestamp(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    message_with_timestamp = array(
        "B",
        [
            0xAA,
            0x18,
            0x01,
            0x00,
            0x8A,
            0x02,
            0x00,
            0x00,
            0x00,
            0x0F,
            0x06,
            0x00,
            0x4B,
            0x00,
            0xEF,
            0xFF,
            0x00,
            0x00,
            0x16,
            0x3D,
            0x8C,
            0xBA,
            0x0D,
            0x0A,
        ],
    )
    response = streaming_interrupt_command.parse_streaming_packet(message_with_timestamp, includes_mcu_timestamp=True)
    sensor_id, packet_count, timestamp, payload = response
    assert sensor_id == 2
    assert packet_count == 0xF
    assert timestamp == 12437749
    assert payload == array("B", (0x06, 0x00, 0x4B, 0x00, 0xEF, 0xFF))
