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
def test_command_stop_interrupt_streaming_parse(streaming_interrupt_command: StreamingInterruptCmd) -> None:
    dummy_response = array("B", (0xCA, 0xFE))

    assert streaming_interrupt_command.parse(dummy_response) is None


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
