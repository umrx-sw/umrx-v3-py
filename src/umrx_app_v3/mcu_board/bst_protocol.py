import logging
from array import array
from typing import Any

from umrx_app_v3.mcu_board.comm.serial_comm import SerialCommunication
from umrx_app_v3.mcu_board.comm.usb_comm import UsbCommunication

logger = logging.getLogger(__name__)


class BstProtocolError(Exception): ...


class BstProtocol:
    def __init__(self, **kw: Any) -> None:
        self.communication: SerialCommunication | UsbCommunication | None = None
        if kw.get("comm"):
            if kw["comm"] == "usb":
                if kw.get("usb") and isinstance(kw["usb"], UsbCommunication):
                    self.communication = kw["usb"]
                else:
                    self.communication = UsbCommunication()
            elif kw["comm"] == "serial":
                if kw.get("serial") and isinstance(kw["serial"], SerialCommunication):
                    self.communication = kw["serial"]
                else:
                    self.communication = SerialCommunication()
            else:
                error_message = f"Provided communication type {kw['comm']} is not supported"
                raise BstProtocolError(error_message)

    def initialize(self) -> None:
        self.communication.connect()

    def send(self, message: array | tuple | list) -> bool:
        return self.communication.send(message)

    def receive(self) -> array | bytes:
        return self.communication.receive()

    def send_receive(self, message: array | tuple | list) -> array | bytes:
        return self.communication.send_receive(message)
