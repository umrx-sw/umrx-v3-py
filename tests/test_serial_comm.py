import logging

import pytest

from array import array
from umrx_app_v3.mcu_board.comm.serial_comm import SerialCommunication

logger = logging.getLogger(__name__)


def test_serial_comm_init(serial_comm: SerialCommunication):
    assert isinstance(serial_comm, SerialCommunication), f"Expect `SerialCommunication` got {type(serial_comm)}"
    assert serial_comm.port is None
