import logging
import sys

import serial

from umrx_app_v3.mcu_board.comm.comm import Communication

logger = logging.getLogger(__name__)


class SerialCommunicationError(Exception):
    ...


class SerialCommunication(Communication):
    def __init__(self):
        self.vid = 0x108c  # App Board 3.1
        self.pid = 0xab38
        self.port: serial.Serial | None = None
        self.port_name: str | None = None
        self.buffer_size = 125
        self.is_initialized: bool = False

    def send(self, message):
        bytes_written = self.port.write(message)
        self.port.flush()
        return bytes_written == len(message)

    def receive(self):
        ok = False
        read_from_serial = b""
        while not ok:
            # read until we get something in the buffer
            in_waiting = self.port.in_waiting
            logger.info(f"waiting buffer: {in_waiting}")
            read_from_serial += self.port.read(self.buffer_size)
            logger.info(f"buffer size: {len(read_from_serial)}")
            ok = len(read_from_serial) > 0
        return read_from_serial

    def send_receive(self, message):
        send_ok = self.send(message)
        if not send_ok:
            raise SerialCommunicationError("Sending packet failed!")
        return self.receive()

    def find_device(self):
        match sys.platform:
            case "linux":
                self.find_device_on_linux()
            case "win32":
                raise NotImplementedError("Searching device is not implemented for Windows!")
            case "darwin":
                raise NotImplementedError("Searching device is not implemented for Mac!")
            case _:
                raise NotImplementedError(f"Searching device is not implemented for {sys.platform}!")

    def find_device_on_linux(self):
        import pyudev
        context = pyudev.Context()
        for device in context.list_devices(subsystem="tty"):
            if device.get("ID_VENDOR") == "Bosch_Sensortec_GmbH":
                self.port_name = device.device_node
                logger.info(f"Found serial device: port={self.port_name}")
                return True
        return False

    def initialize(self):
        if self.port_name is None:
            self.find_device()
        self.port = serial.Serial(port=self.port_name)
        self.port.port = self.port_name
        self.port.baudrate = 115200
        if not self.port.is_open:
            self.port.open()

    def connect(self):
        if not self.is_initialized:
            self.initialize()

    def disconnect(self):
        pass
