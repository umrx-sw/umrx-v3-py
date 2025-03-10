import logging
from array import array
from unittest.mock import patch, PropertyMock

import pytest
import usb.core

from umrx_app_v3.mcu_board.comm.usb_comm import UsbCommunication, UsbCommunicationError

logger = logging.getLogger(__name__)


@pytest.mark.usb_comm
def test_usb_comm_construction(usb_comm: UsbCommunication) -> None:
    assert usb_comm.vid == 0x152A, "Wrong vendor ID"
    assert usb_comm.pid == 0x80C0, "Wrong product ID"
    assert usb_comm.is_initialized is False, "Should not be initialized on creation"


@pytest.mark.usb_comm
def test_usb_comm_find_device(usb_comm: UsbCommunication) -> None:
    with patch.object(usb.core, "find") as mock_find:
        usb_comm.find_device()
    mock_find.assert_called_once()


@pytest.mark.usb_comm
def test_usb_comm_find_device_raises(usb_comm: UsbCommunication) -> None:
    with pytest.raises(UsbCommunicationError), patch.object(usb.core, "find", return_value=None):
        usb_comm.find_device()


@pytest.mark.usb_comm
def test_usb_comm_bulk_in_packet_size(usb_comm: UsbCommunication) -> None:
    with patch.object(usb_comm, "endpoint_bulk_in", PropertyMock()):
        usb_comm.endpoint_bulk_in = None
        assert usb_comm.bulk_in_packet_size == -1, "Expect to get -1 for non-existing endpoint"


@pytest.mark.usb_comm
def test_usb_comm_send_empty_msg(usb_comm: UsbCommunication) -> None:
    ok = usb_comm.send([])
    assert ok is False, "Do not expect OK when sending empty message"


@pytest.mark.usb_comm
def test_usb_comm_send_well_formatted_message(usb_comm: UsbCommunication) -> None:
    with (
        patch.object(usb_comm, "create_packet_from", return_value=array("B", [1, 2, 3])),
        patch.object(usb_comm, "endpoint_bulk_out") as mock_endpoint_bulk_out,
    ):
        message = array("B", [3, 2, 1])
        mock_endpoint_bulk_out.write.return_value = 3
        ok = usb_comm.send(message)
    assert ok, " OK when sending good message"


@pytest.mark.usb_comm
def test_usb_comm_serialize_baud_rate_1200(usb_comm: UsbCommunication) -> None:
    res = usb_comm.serialize_baud_rate(1200)
    assert res == (0xB0, 0x04, 0x00, 0x00, 0x00, 0x00, 0x08), "Serialized wrong"


@pytest.mark.usb_comm
def test_usb_comm_serialize_baud_rate_little_endian(usb_comm: UsbCommunication) -> None:
    res = usb_comm.serialize_baud_rate(0xAABBCCDD)
    assert res == (0xDD, 0xCC, 0xBB, 0xAA, 0x00, 0x00, 0x08), "Serialized wrong"


@pytest.mark.usb_comm
def test_usb_comm_control_transfer(usb_comm: UsbCommunication) -> None:
    with (
        patch.object(usb_comm, "usb_device"),
        patch.object(usb_comm.usb_device, "ctrl_transfer") as mocked_ctrl_transfer,
        patch("time.sleep", return_value=None),
    ):
        usb_comm.send_control_transfer(1200)

        assert mocked_ctrl_transfer.call_count == 6, "Wrong number of calls"


# @pytest.mark.usb_comm
# def test_usb_comm_recv(usb_comm: UsbCommunication):
#     data = usb_comm.receive()
#     assert type(data) == array, f"Expecting `array` of bytes back"
#
#
# @pytest.mark.usb_comm
# def test_usb_comm_send(usb_comm: UsbCommunication):
#     packet_payload = 170, 6, 2, 31, 13, 10,
#     packet_payload_array = array('B', packet_payload)
#     packet_to_send = array('B', 64 * [0])
#     packet_to_send[0:len(packet_payload_array)] = packet_payload_array
#     ok = usb_comm.send(packet_to_send)
#     assert ok, f"Sending packet failed!"


@pytest.mark.usb_comm
def test_usb_comm_create_packet_from(usb_comm: UsbCommunication) -> None:
    def check_result(result: array, initial_content: array | tuple | list) -> None:
        assert isinstance(result, array), "Expecting array of bytes to send"
        assert len(result) == usb_comm.bulk_out_packet_size, "Expecting packet siz of equal endpoint's wMaxPacketSize"
        assert result[0 : len(initial_content)] == array("B", initial_content), "Start content shall be equal"
        assert all(el == 255 for el in result[len(initial_content) :]), "End of the packet shall be filled"

    with patch.object(usb_comm, "endpoint_bulk_out") as mock_endpoint_bulk_out:
        mock_endpoint_bulk_out.wMaxPacketSize = 64

        packet_payload_tuple = 170, 6, 2, 31, 13, 10
        packet = usb_comm.create_packet_from(packet_payload_tuple)
        check_result(packet, packet_payload_tuple)

        packet_payload_list = [170, 6, 2, 31, 13, 10]
        packet = usb_comm.create_packet_from(packet_payload_list)
        check_result(packet, packet_payload_list)

        packet_payload_array = array("B", [170, 6, 2, 31, 13, 10])
        packet = usb_comm.create_packet_from(packet_payload_array)
        check_result(packet, packet_payload_array)

        empty_packet = []
        packet = usb_comm.create_packet_from(empty_packet)
        check_result(packet, empty_packet)
