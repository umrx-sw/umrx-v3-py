import logging
from array import array

import pytest
import usb.core

from umrx_app_v3.mcu_board.comm.usb_comm import UsbCommunication

logger = logging.getLogger(__name__)


@pytest.mark.usb_comm
def test_usb_comm_construction(usb_comm: UsbCommunication):
    assert usb_comm.vid == 0x152a and usb_comm.pid == 0x80c0, "Expected VID & PID for App Board 3.0 wrong"
    assert usb_comm.is_initialized, "Should be initialized after creation"
    assert isinstance(usb_comm.endpoint_bulk_in, usb.core.Endpoint), "Unexpected endpoint type"
    assert isinstance(usb_comm.endpoint_bulk_out, usb.core.Endpoint), "Unexpected endpoint type"


@pytest.mark.usb_comm
def test_usb_comm_endpoint_packet(usb_comm: UsbCommunication):
    assert usb_comm.bulk_in_packet_size == 64, "Invalid packet size for bulk IN"
    assert usb_comm.bulk_out_packet_size == 64, "Invalid packet size for bulk OUT"


@pytest.mark.usb_comm
def test_usb_comm_recv(usb_comm: UsbCommunication):
    data = usb_comm.receive()
    assert isinstance(data, array), "Expecting `array` of bytes back"


@pytest.mark.usb_comm
def test_usb_comm_send(usb_comm: UsbCommunication):
    packet_payload = 170, 6, 2, 31, 13, 10,
    packet_payload_array = array("B", packet_payload)
    packet_to_send = array("B", 64 * [0])
    packet_to_send[0:len(packet_payload_array)] = packet_payload_array
    ok = usb_comm.send(packet_to_send)
    assert ok, "Sending packet failed!"
