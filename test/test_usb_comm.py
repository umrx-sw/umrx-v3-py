import logging
from typing import Union, Tuple, List

import pytest
import usb.core

from array import array
from umrx_app_v3.mcu_board.usb_comm import UsbCommunication

logger = logging.getLogger()


@pytest.mark.usb_comm
def test_usb_comm_construction(usb_comm: UsbCommunication):
    assert usb_comm.vid == 0x152a and usb_comm.pid == 0x80c0, "Expected VID & PID wrong"
    assert usb_comm.is_initialized, "Should be initialized after creation"
    assert isinstance(usb_comm.endpoint_bulk_in, usb.core.Endpoint), "Unexpected endpoint type"
    assert isinstance(usb_comm.endpoint_bulk_out, usb.core.Endpoint), "Unexpected endpoint type"


@pytest.mark.usb_comm
def test_usb_comm_endpoint_packet(usb_comm: UsbCommunication):
    assert usb_comm.bulk_in_packet_size == 64, f"Invalid packet size for bulk IN"
    assert usb_comm.bulk_out_packet_size == 64, f"Invalid packet size for bulk OUT"


@pytest.mark.usb_comm
def test_usb_comm_recv(usb_comm: UsbCommunication):
    data = usb_comm.recv()
    assert len(data) == usb_comm.bulk_in_packet_size, f"Expected {usb_comm.bulk_in_packet_size} bytes, got {len(data)}"
    assert type(data) == array, f"Expecting `array` of bytes back"


@pytest.mark.usb_comm
def test_usb_comm_send(usb_comm: UsbCommunication):
    packet_payload = 170, 6, 2, 31, 13, 10,
    packet_payload_array = array('B', packet_payload)
    packet_to_send = array('B', 64 * [0])
    packet_to_send[0:len(packet_payload_array)] = packet_payload_array
    ok = usb_comm.send(packet_to_send)
    assert ok, f"Sending packet failed!"


@pytest.mark.usb_comm
def test_usb_comm_create_packet_from(usb_comm: UsbCommunication):

    def check_result(result: array, initial_content: Union[array, Tuple, List]):
        assert isinstance(result, array), "Expecting array of bytes to send"
        assert len(result) == usb_comm.bulk_out_packet_size, "Expecting packet siz of equal endpoint's wMaxPacketSize"
        assert result[0:len(initial_content)] == array('B', initial_content), "Start content shall be equal"
        assert all(el == 255 for el in result[len(initial_content):]), "End of the packet shall be filled"

    packet_payload_tuple = 170, 6, 2, 31, 13, 10,
    packet = usb_comm.create_packet_from(packet_payload_tuple)
    check_result(packet, packet_payload_tuple)

    packet_payload_list = [170, 6, 2, 31, 13, 10,]
    packet = usb_comm.create_packet_from(packet_payload_list)
    check_result(packet, packet_payload_list)

    packet_payload_array = array('B', [170, 6, 2, 31, 13, 10,])
    packet = usb_comm.create_packet_from(packet_payload_array)
    check_result(packet, packet_payload_array)

    empty_packet = []
    packet = usb_comm.create_packet_from(empty_packet)
    check_result(packet, empty_packet)
