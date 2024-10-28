import logging
from array import array
from unittest.mock import patch

import pytest

from umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from umrx_app_v3.mcu_board.comm.usb_comm import UsbCommunication

logger = logging.getLogger(__name__)


@pytest.mark.bst_protocol
def test_bst_protocol_construction(bst_protocol_usb: BstProtocol) -> None:
    assert isinstance(bst_protocol_usb, BstProtocol), "Expecting instance of BstProcotol"
    assert isinstance(bst_protocol_usb.communication, UsbCommunication), "Expect USB communication protocol"


@pytest.mark.bst_protocol
def test_bst_protocol_check_packet(bst_protocol_usb: BstProtocol) -> None:
    with patch.object(bst_protocol_usb.communication, "endpoint_bulk_out") as mock_endpoint_bulk_out:
        mock_endpoint_bulk_out.wMaxPacketSize = 64
        valid_packet = 170, 6, 2, 31, 13, 10
        valid_packet_filled = bst_protocol_usb.communication.create_packet_from(valid_packet)
        should_be_valid = bst_protocol_usb.communication.check_message(valid_packet_filled)
        assert should_be_valid, "Check of valid packet shall pass"

        wrong_length_packet = 170, 4, 3, 45, 11, 22, 13, 10
        wrong_length_packet_filled = bst_protocol_usb.communication.create_packet_from(wrong_length_packet)
        should_be_invalid = bst_protocol_usb.communication.check_message(wrong_length_packet_filled)
        assert not should_be_invalid, "Check of invalid packet shall fail"

        wrong_zero_data_received = 0, 0, 0, 0, 0, 0, 0
        wrong_zero_data_received_filled = bst_protocol_usb.communication.create_packet_from(wrong_zero_data_received)
        should_be_invalid = bst_protocol_usb.communication.check_message(wrong_zero_data_received_filled)
        assert not should_be_invalid, "Check of wrong 0x00 data shall fail"

        wrong_ff_data_received = 255, 255, 255, 255, 255, 255, 255
        wrong_ff_data_received_filled = bst_protocol_usb.communication.create_packet_from(wrong_ff_data_received)
        should_be_invalid = bst_protocol_usb.communication.check_message(wrong_ff_data_received_filled)
        assert not should_be_invalid, "Check of wrong 0xFF data shall fail"


@pytest.mark.bst_protocol
def test_bst_protocol_extract_message_from(bst_protocol_usb: BstProtocol) -> None:
    packet = array(
        "B",
        [
            170,
            15,
            1,
            0,
            66,
            31,
            0,
            102,
            0,
            16,
            0,
            9,
            5,
            13,
            10,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
        ],
    )
    message = bst_protocol_usb.communication.extract_message_from(packet)
    assert len(message) == int(packet[1]), "Wrong length of the extracted message"
    assert message[0] == 0xAA, "Wrong start of the packet"
    assert message[-2] == 0x0D, "Wrong end of the packet"
    assert message[-1] == 0x0A, "Wrong end of the packet"


@pytest.mark.bst_protocol
def test_bst_protocol_create_message_from(bst_protocol_usb: BstProtocol) -> None:
    def check_result(result: array, payload: array | tuple | list) -> None:
        assert isinstance(result, array), "Expecting message as array"
        assert len(result) == len(payload) + 4, "Expecting message size does not match"
        assert result[2 : 2 + len(payload)] == array("B", payload), "Incorrect payload in the message"
        assert result[0] == 0xAA, "Start byte of message invalid"
        assert result[1] == len(result), "Message length is wrong in the message"
        assert result[-2] == 0xD, "Message stop sequence invalid"
        assert result[-1] == 0xA, "Message stop sequence invalid"

    payload_tuple = 2, 31
    message = bst_protocol_usb.create_message_from(payload_tuple)
    check_result(message, payload_tuple)

    payload_list = [2, 31]
    message = bst_protocol_usb.create_message_from(payload_list)
    check_result(message, payload_list)

    payload_array = array("B", [2, 31])
    message = bst_protocol_usb.create_message_from(payload_array)
    check_result(message, payload_array)
