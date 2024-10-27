import logging

import pytest

from array import array
from umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from umrx_app_v3.mcu_board.comm.usb_comm import UsbCommunication

logger = logging.getLogger(__name__)


@pytest.mark.bst_protocol
def test_bst_protocol_send(bst_protocol_usb: BstProtocol):
    valid_packet = 170, 6, 2, 31, 13, 10,
    ok = bst_protocol_usb.send(valid_packet)
    assert ok, "Sending packet failed"


@pytest.mark.bst_protocol
def test_bst_protocol_recv(bst_protocol_usb: BstProtocol):
    valid_packet = 170, 6, 2, 31, 13, 10,
    ok = bst_protocol_usb.send(valid_packet)
    assert ok, "Sending board info request packet failed!"
    reply = bst_protocol_usb.receive()
    expected_reply = 170, 15, 1, 0, 66, 31, 0, 102, 0, 16, 0, 25, 5, 13, 10,
    expected_reply = 170, 15, 1, 0, 66, 31, 1, 65, 0, 16, 0, 9, 5, 13, 10,
    assert isinstance(reply, array), "Expecting an array back"
    assert tuple(reply[:len(expected_reply)]) == expected_reply, "Expecting App Board 3.0 + BMI08x reply back"
