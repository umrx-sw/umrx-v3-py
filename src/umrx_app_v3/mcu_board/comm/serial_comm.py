import logging
from array import array
from collections.abc import Generator
from typing import Any

import serial
import serial.tools.list_ports

from umrx_app_v3.mcu_board.comm.comm import Communication
from umrx_app_v3.mcu_board.commands.command import Command

logger = logging.getLogger(__name__)


class SerialCommunicationError(Exception): ...


class SerialCommunication(Communication):
    def __init__(self, **kw: Any) -> None:
        self.vid = kw["vid"] if kw.get("vid") else 0x108C  # App Board 3.1
        self.pid = kw["pid"] if kw.get("pid") else 0xAB38
        self.port: serial.Serial | None = None
        self.port_name: str | None = None
        self.buffer_size = 125
        self.is_initialized: bool = False

    def send(self, message: array[int] | list[int] | tuple[int, ...]) -> bool:
        bytes_written = self.port.write(message)
        self.port.flush()
        return bytes_written == len(message)

    def _receive(self) -> array[int] | bytes:
        ok = False
        read_from_serial = b""
        while not ok:
            # read until we get something in the buffer
            in_waiting = self.port.in_waiting
            # logger.info(f"waiting buffer: {in_waiting}")
            read_from_serial += self.port.read(in_waiting)
            # logger.info(f"buffer size: {len(read_from_serial)}")
            ok = len(read_from_serial) > 0
        return read_from_serial

    def receive(self) -> array[int] | bytes:
        return self._receive()

    def receive_multiple_streaming_packets(self) -> Generator:
        message = self._receive()
        while len(message) > 0:
            if Command.check_message(message):
                packet_len = message[1]
                packet = message[:packet_len]
                message = message[packet_len:]
                yield packet
            else:
                possible_start_idx = message.find(0x0A)
                if (
                    possible_start_idx == -1
                    or len(message) < possible_start_idx + 2
                    or len(message) < message[possible_start_idx + 2] + 2
                ):
                    break
                else:
                    message = message[possible_start_idx + 1 :]

    def send_receive(self, message: array[int] | tuple[int, ...] | list[int]) -> array | bytes:
        send_ok = self.send(message)
        if not send_ok:
            error_message = "Sending packet failed!"
            raise SerialCommunicationError(error_message)
        return self.receive()

    def find_device(self) -> bool:
        ports = serial.tools.list_ports.comports()
        for port_info in sorted(ports):
            if port_info.vid == self.vid and port_info.pid == self.pid:
                self.port_name = port_info.device
                logger.debug(f"Found board: port={self.port_name}")
                return True
        return False

    def initialize(self) -> None:
        if self.port_name is None:
            found = self.find_device()
            if not found:
                error_msg = "Board is not found! Is it connected and turned ON?"
                raise SerialCommunicationError(error_msg)
        self.port = serial.Serial(port=self.port_name)
        self.port.port = self.port_name
        self.port.baudrate = 115200
        if not self.port.is_open:
            self.port.open()

    def connect(self) -> None:
        if not self.is_initialized:
            self.initialize()

    def disconnect(self) -> None:
        pass
