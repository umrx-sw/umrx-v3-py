import logging
import sys
from array import array

import serial

from umrx_app_v3.mcu_board.comm.comm import Communication

logger = logging.getLogger(__name__)


class SerialCommunicationError(Exception): ...


class SerialCommunication(Communication):
    def __init__(self) -> None:
        self.vid = 0x108C  # App Board 3.1
        self.pid = 0xAB38
        self.port: serial.Serial | None = None
        self.port_name: str | None = None
        self.buffer_size = 125
        self.is_initialized: bool = False

    def send(self, message: array | list | tuple) -> bool:
        bytes_written = self.port.write(message)
        self.port.flush()
        return bytes_written == len(message)

    def receive(self) -> array | bytes:
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

    def send_receive(self, message: array | tuple | list) -> array | bytes:
        send_ok = self.send(message)
        if not send_ok:
            error_message = "Sending packet failed!"
            raise SerialCommunicationError(error_message)
        return self.receive()

    def find_device(self) -> bool:
        match sys.platform:
            case "linux":
                return self.find_device_on_linux()
            case "win32":
                error_message = "Searching device is not implemented for Windows!"
                raise NotImplementedError(error_message)
            case "darwin":
                error_message = "Searching device is not implemented for Mac!"
                raise NotImplementedError(error_message)
            case _:
                error_message = f"Searching device is not implemented for {sys.platform}!"
                raise NotImplementedError(error_message)

    def find_device_on_linux(self) -> bool:
        import pyudev

        context = pyudev.Context()
        for device in context.list_devices(subsystem="tty"):
            if int(device.get("ID_MODEL_ID"), 16) == self.pid and int(device.get("ID_VENDOR_ID"), 16) == self.vid:
                self.port_name = device.device_node
                logger.debug(f"Found board: port={self.port_name}")
                return True
        return False

    def initialize(self) -> None:
        if self.port_name is None:
            self.find_device()
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
