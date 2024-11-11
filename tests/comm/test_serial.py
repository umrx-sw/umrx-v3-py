import logging
from pathlib import Path
from unittest.mock import patch

from umrx_app_v3.mcu_board.comm.serial_comm import SerialCommunication

logger = logging.getLogger(__name__)


def test_serial_comm_init(serial_comm: SerialCommunication) -> None:
    assert isinstance(serial_comm, SerialCommunication), f"Expect `SerialCommunication` got {type(serial_comm)}"
    assert serial_comm.port is None


def test_serial_message_split(serial_comm: SerialCommunication) -> None:
    current_folder = Path(__file__).parent
    with Path.open(current_folder / "message.bytes", "rb") as f:
        message = f.read()
    assert message
    with patch.object(serial_comm, "_receive", return_value=message):
        num_packets = 0
        for _ in serial_comm.receive_streaming():
            num_packets += 1
        assert num_packets == 272
