
from umrx_app_v3.mcu_board.comm.comm import Communication
import serial


class SerialCommunication(Communication):
    def __init__(self):
        self.vid = 0x108c  # App Board 3.1
        self.pid = 0xab38
        self.port: serial.Serial | None = None

    def send(self, message):
        pass

    def receive(self):
        pass

    def send_receive(self, message):
        pass

    def find_device(self):
        pass

    def initialize(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass
