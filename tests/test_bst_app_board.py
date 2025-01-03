import logging
import time
from array import array
from unittest.mock import patch

import pytest

from umrx_app_v3.mcu_board.bst_app_board import ApplicationBoard
from umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from umrx_app_v3.mcu_board.bst_protocol_constants import (
    I2CMode,
    MultiIOPin,
    PinDirection,
    PinValue,
    SPISpeed,
    StreamingSamplingUnit,
)
from umrx_app_v3.mcu_board.comm.serial_comm import SerialCommunication
from umrx_app_v3.mcu_board.commands.spi import SPIConfigureCmd
from umrx_app_v3.mcu_board.commands.streaming_interrupt import (
    StreamingInterruptCmd,
    StreamingInterruptI2cChannelConfig,
    StreamingInterruptI2cConfig,
    StreamingInterruptSpiChannelConfig,
    StreamingInterruptSpiConfig,
)
from umrx_app_v3.mcu_board.commands.streaming_polling import StreamingPollingCmd

logger = logging.getLogger(__name__)


@pytest.mark.app_board
def test_app_board_construction(bst_app_board_with_serial: ApplicationBoard) -> None:
    assert isinstance(bst_app_board_with_serial, ApplicationBoard), "Expecting instance of ApplicationBoard30"
    assert isinstance(bst_app_board_with_serial.protocol, BstProtocol), "Expect BST protocol object inside App Board"
    assert isinstance(bst_app_board_with_serial.protocol.communication, SerialCommunication), "Expecting Serial"


@pytest.mark.app_board
def test_app_board_vdd_vddio(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.set_vdd_vddio(1.8, 3.3)
        arg = array("B", [0xAA, 0x0C, 0x01, 0x14, 0x07, 0x08, 0x01, 0x0C, 0xE4, 0x01, 0x0D, 0x0A])
        mocked_send_receive.assert_called_with(arg)


@pytest.mark.app_board
def test_app_board_board_info(bst_app_board_with_serial: ApplicationBoard) -> None:
    resp = array("B", [0xAA, 0x0F, 0x01, 0x00, 0x42, 0x1F, 0x01, 0x41, 0x00, 0x10, 0x00, 0x09, 0x05, 0x0D, 0x0A])

    with patch.object(
        bst_app_board_with_serial.protocol.communication, "send_receive", return_value=resp
    ) as mocked_send_receive:
        info = bst_app_board_with_serial.board_info
        logger.info("info = %s", info)
        command_to_send = array("B", [0xAA, 0x06, 0x02, 0x1F, 0x0D, 0x0A])
        mocked_send_receive.assert_called_with(command_to_send)


@pytest.mark.app_board
def test_app_board_disable_timer(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol.communication, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.disable_timer()
        assert mocked_send_receive.call_count == 2


@pytest.mark.app_board
def test_app_board_enable_timer(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol.communication, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.enable_timer()
        assert mocked_send_receive.call_count == 2


@pytest.mark.app_board
def test_app_board_stop_polling_streaming(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol.communication, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.stop_polling_streaming()
        command_to_send = array("B", [0xAA, 0x06, 0x06, 0x00, 0x0D, 0x0A])
        mocked_send_receive.assert_called_with(command_to_send)


@pytest.mark.app_board
def test_app_board_stop_interrupt_streaming(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol.communication, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.stop_interrupt_streaming()
        command_to_send = array("B", [0xAA, 0x06, 0x0A, 0x00, 0x0D, 0x0A])
        mocked_send_receive.assert_called_with(command_to_send)


@pytest.mark.app_board
def test_app_board_app_switch(bst_app_board_with_serial: ApplicationBoard) -> None:
    with (
        patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive,
    ):
        bst_app_board_with_serial.switch_app(0xAABB)
        mocked_send_receive.assert_called_once()


@pytest.mark.app_board
def test_app_board_switch_usb_mtp(bst_app_board_with_serial: ApplicationBoard) -> None:
    with (
        patch.object(bst_app_board_with_serial, "start_communication") as mocked_start_communication,
        patch.object(bst_app_board_with_serial, "switch_app") as mocked_switch_app,
    ):
        bst_app_board_with_serial.switch_usb_mtp()
        mocked_start_communication.assert_called_once()
        mocked_switch_app.assert_called_once()


@pytest.mark.app_board
def test_app_board_switch_usb_dfu_bl(bst_app_board_with_serial: ApplicationBoard) -> None:
    with (
        patch.object(bst_app_board_with_serial, "start_communication") as mocked_start_communication,
        patch.object(bst_app_board_with_serial, "switch_app") as mocked_switch_app,
    ):
        bst_app_board_with_serial.switch_usb_dfu_bl()
        mocked_start_communication.assert_called_once()
        mocked_switch_app.assert_called_once()


@pytest.mark.app_board
def test_app_board_configure_i2c(bst_app_board_with_serial: ApplicationBoard) -> None:
    with (
        patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive,
    ):
        bst_app_board_with_serial.configure_i2c(I2CMode.STANDARD_MODE)
        assert mocked_send_receive.call_count == 2


@pytest.mark.app_board
def test_app_board_read_i2c(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(
        bst_app_board_with_serial.protocol,
        "send_receive",
        return_value=array("B", (0xAA, 0x0E, 0x01, 0x00, 0x42, 0x16, 0x01, 0x00, 0x01, 0x01, 0x00, 0x1E, 0x0D, 0x0A)),
    ):
        resp = bst_app_board_with_serial.read_i2c(0x18, 0x0, 0x1)

        assert resp == array("B", (0x1E,))


@pytest.mark.app_board
def test_app_board_write_i2c(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(
        bst_app_board_with_serial.protocol,
        "send_receive",
    ) as mocked_send_receive:
        bst_app_board_with_serial.write_i2c(0x68, 0x0F, array("B", (0x03,)))

        expected_payload = array(
            "B",
            (
                0xAA,
                0x13,
                0x01,
                0x16,
                0x01,
                0x00,
                0x01,
                0x01,
                0x00,
                0x68,
                0x0F,
                0x00,
                0x01,
                0x01,
                0x00,
                0x00,
                0x03,
                0x0D,
                0x0A,
            ),
        )
        mocked_send_receive.assert_called_with(expected_payload)


@pytest.mark.app_board
def test_app_board_start_communication(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol, "send_receive"), patch.object(time, "sleep"):
        bst_app_board_with_serial.start_communication()


@pytest.mark.app_board
def test_app_board_set_pin_config(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.set_pin_config(
            pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1, direction=PinDirection.OUTPUT, value=PinValue.HIGH
        )

        expected_payload = array("B", (0xAA, 0x0C, 0x01, 0x15, 0x80, 0x16, 0x00, 0x01, 0x00, 0x01, 0x0D, 0x0A))
        mocked_send_receive.assert_called_with(expected_payload)


@pytest.mark.app_board
def test_app_board_get_pin_config(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(
        bst_app_board_with_serial.protocol,
        "send_receive",
        return_value=array("B", (0xAA, 0x0E, 0x01, 0x00, 0x42, 0x15, 0x00, 0x16, 0x00, 0x01, 0x00, 0x00, 0x0D, 0x0A)),
    ):
        direction, value = bst_app_board_with_serial.get_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6)
        assert direction == PinDirection.OUTPUT
        assert value == PinValue.LOW


@pytest.mark.app_board
def test_app_board_configure_spi(bst_app_board_with_serial: ApplicationBoard) -> None:
    with (
        patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive,
        patch.object(SPIConfigureCmd, "parse"),
    ):
        bst_app_board_with_serial.configure_spi(SPISpeed.MHz_5)
        assert mocked_send_receive.call_count == 2


@pytest.mark.app_board
def test_app_board_read_spi(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(
        bst_app_board_with_serial.protocol,
        "send_receive",
        return_value=array(
            "B",
            (
                0xAA,
                0x13,
                0x01,
                0x00,
                0x42,
                0x16,
                0x01,
                0x82,
                0x06,
                0x01,
                0x00,
                0x3F,
                0x00,
                0xFE,
                0xFF,
                0x17,
                0x00,
                0x0D,
                0x0A,
            ),
        ),
    ):
        resp = bst_app_board_with_serial.read_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_5, 0x02, 0x06)

        assert resp == array("B", (0x3F, 0x00, 0xFE, 0xFF, 0x17, 0x00))


@pytest.mark.app_board
def test_app_board_write_spi(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(
        bst_app_board_with_serial.protocol,
        "send_receive",
    ) as mocked_send_receive:
        bst_app_board_with_serial.write_spi(
            cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1, start_register_address=0x7D, data_to_write=array("B", (0x04,))
        )

        expected_payload = array(
            "B",
            (
                0xAA,
                0x13,
                0x01,
                0x16,
                0x01,
                0x16,
                0x01,
                0x01,
                0x00,
                0x00,
                0x7D,
                0x00,
                0x01,
                0x01,
                0x00,
                0x00,
                0x04,
                0x0D,
                0x0A,
            ),
        )
        mocked_send_receive.assert_called_with(expected_payload)


@pytest.mark.app_board
def test_app_board_set_streaming_polling_i2c(bst_app_board_with_serial: ApplicationBoard) -> None:
    bst_app_board_with_serial.streaming_polling_set_i2c_configuration()

    assert StreamingPollingCmd.polling_streaming_config is not None

    assert len(StreamingPollingCmd.polling_streaming_config.channel_configs) == 0


@pytest.mark.app_board
def test_app_board_set_streaming_polling_spi(bst_app_board_with_serial: ApplicationBoard) -> None:
    bst_app_board_with_serial.streaming_polling_set_spi_configuration()

    assert StreamingPollingCmd.polling_streaming_config is not None

    assert len(StreamingPollingCmd.polling_streaming_config.channel_configs) == 0


@pytest.mark.app_board
def test_app_board_polling_configure_i2c_2_channel(bst_app_board_with_serial: ApplicationBoard) -> None:
    bst_app_board_with_serial.streaming_polling_set_i2c_configuration()

    bst_app_board_with_serial.streaming_polling_set_i2c_channel(
        i2c_address=0x18,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=6,
    )

    bst_app_board_with_serial.streaming_polling_set_i2c_channel(
        i2c_address=0x68,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )

    assert len(StreamingPollingCmd.polling_streaming_config.channel_configs) == 2

    with patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.configure_streaming_polling(interface="i2c")

        assert mocked_send_receive.call_count == 3


@pytest.mark.app_board
def test_app_board_polling_configure_i2c_1_channel(bst_app_board_with_serial: ApplicationBoard) -> None:
    bst_app_board_with_serial.streaming_polling_set_i2c_configuration()

    bst_app_board_with_serial.streaming_polling_set_i2c_channel(
        i2c_address=0x18,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=6,
    )

    assert len(StreamingPollingCmd.polling_streaming_config.channel_configs) == 1

    with patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.configure_streaming_polling(interface="i2c")

        assert mocked_send_receive.call_count == 2


@pytest.mark.app_board
def test_app_board_polling_configure_spi_2_channel(bst_app_board_with_serial: ApplicationBoard) -> None:
    bst_app_board_with_serial.streaming_polling_set_spi_configuration()

    bst_app_board_with_serial.streaming_polling_set_spi_channel(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=7,
    )

    bst_app_board_with_serial.streaming_polling_set_spi_channel(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )

    assert len(StreamingPollingCmd.polling_streaming_config.channel_configs) == 2

    with patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.configure_streaming_polling(interface="spi")

        assert mocked_send_receive.call_count == 3


@pytest.mark.app_board
def test_app_board_start_polling_streaming(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.start_polling_streaming()
        expected_payload = array("B", (0xAA, 0x06, 0x06, 0xFF, 0x0D, 0x0A))
        mocked_send_receive.assert_called_once_with(expected_payload)


@pytest.mark.app_board
def test_app_board_streaming_polling_receive_i2c(bst_app_board_with_serial: ApplicationBoard) -> None:
    example_streaming_packet = array(
        "B", (0xAA, 0x0F, 0x01, 0x00, 0x87, 0xE4, 0xFF, 0xDE, 0xFF, 0xE8, 0xFF, 0x00, 0x02, 0x0D, 0x0A)
    )
    with patch.object(bst_app_board_with_serial.protocol, "receive", return_value=example_streaming_packet):
        sensor_id, payload = bst_app_board_with_serial.receive_polling_streaming()
        assert sensor_id == 2
        assert payload == array("B", (0xE4, 0xFF, 0xDE, 0xFF, 0xE8, 0xFF))


@pytest.mark.app_board
def test_app_board_start_interrupt_streaming(bst_app_board_with_serial: ApplicationBoard) -> None:
    with patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.start_interrupt_streaming()
        expected_payload = array("B", (0xAA, 0x06, 0x0A, 0xFF, 0x0D, 0x0A))
        mocked_send_receive.assert_called_once_with(expected_payload)


@pytest.mark.app_board
def test_app_board_interrupt_set_spi_config(bst_app_board_with_serial: ApplicationBoard) -> None:
    bst_app_board_with_serial.streaming_interrupt_set_spi_configuration()

    assert isinstance(StreamingInterruptCmd.streaming_interrupt_config, StreamingInterruptSpiConfig)
    assert len(StreamingInterruptCmd.streaming_interrupt_config.channel_configs) == 0


@pytest.mark.app_board
def test_app_board_interrupt_config_spi_channel(bst_app_board_with_serial: ApplicationBoard) -> None:
    config_1 = StreamingInterruptSpiChannelConfig(
        id=1,
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        register_address=0x12,
        bytes_to_read=7,
    )
    bst_app_board_with_serial.streaming_interrupt_set_spi_configuration()
    bst_app_board_with_serial.streaming_interrupt_set_spi_channel(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6,
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        register_address=0x12,
        bytes_to_read=7,
    )

    assert StreamingInterruptCmd.streaming_interrupt_config.channel_configs[0] == config_1


@pytest.mark.app_board
def test_app_board_interrupt_set_i2c_config(bst_app_board_with_serial: ApplicationBoard) -> None:
    bst_app_board_with_serial.streaming_interrupt_set_i2c_configuration()

    assert isinstance(StreamingInterruptCmd.streaming_interrupt_config, StreamingInterruptI2cConfig)
    assert len(StreamingInterruptCmd.streaming_interrupt_config.channel_configs) == 0


@pytest.mark.app_board
def test_app_board_interrupt_config_i2c_channel(bst_app_board_with_serial: ApplicationBoard) -> None:
    config_1 = StreamingInterruptI2cChannelConfig(
        id=1, interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6, i2c_address=0x18, register_address=0x12, bytes_to_read=6
    )
    bst_app_board_with_serial.streaming_interrupt_set_i2c_configuration()
    bst_app_board_with_serial.streaming_interrupt_set_i2c_channel(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6, i2c_address=0x18, register_address=0x12, bytes_to_read=6
    )

    assert StreamingInterruptCmd.streaming_interrupt_config.channel_configs[0] == config_1


@pytest.mark.app_board
def test_app_board_interrupt_configure_streaming(bst_app_board_with_serial: ApplicationBoard) -> None:
    bst_app_board_with_serial.streaming_interrupt_set_i2c_configuration()
    bst_app_board_with_serial.streaming_interrupt_set_i2c_channel(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_6, i2c_address=0x18, register_address=0x12, bytes_to_read=6
    )

    bst_app_board_with_serial.streaming_interrupt_set_i2c_channel(
        interrupt_pin=MultiIOPin.MINI_SHUTTLE_PIN_1_7, i2c_address=0x68, register_address=0x02, bytes_to_read=6
    )

    with patch.object(bst_app_board_with_serial.protocol, "send_receive") as mocked_send_receive:
        bst_app_board_with_serial.configure_streaming_interrupt(interface="i2c")

        assert mocked_send_receive.call_count == 2


@pytest.mark.app_board
def test_app_board_interrupt_receive_streaming(bst_app_board_with_serial: ApplicationBoard) -> None:
    message_without_timestamp = array("B", [170, 18, 1, 0, 138, 2, 0, 0, 1, 238, 228, 255, 191, 255, 205, 255, 13, 10])
    with patch.object(bst_app_board_with_serial.protocol, "receive", return_value=message_without_timestamp):
        streaming_response = bst_app_board_with_serial.receive_interrupt_streaming()
        channel_id, packet_count, timestamp, payload = streaming_response
        assert channel_id == 2
        assert packet_count == 494
        assert timestamp == -1
        assert payload == array("B", (228, 255, 191, 255, 205, 255))

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
    with patch.object(bst_app_board_with_serial.protocol, "receive", return_value=message_with_timestamp):
        streaming_response = bst_app_board_with_serial.receive_interrupt_streaming(includes_mcu_timestamp=True)
        channel_id, packet_count, timestamp, payload = streaming_response
        assert channel_id == 2
        assert packet_count == 0x0F
        assert timestamp == 12437749
        assert payload == array("B", (0x06, 0x00, 0x4B, 0x00, 0xEF, 0xFF))
