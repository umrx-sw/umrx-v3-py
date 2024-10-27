import logging
from array import array

from umrx_app_v3.mcu_board.comm.usb_comm import UsbCommunication
from umrx_app_v3.mcu_board.comm.serial_comm import SerialCommunication

logger = logging.getLogger(__name__)


class BstProtocol:
    def __init__(self, *a, **kw):
        self.communication: SerialCommunication | UsbCommunication | None = None
        if kw.get('comm'):
            if kw['comm'] == 'usb':
                if kw.get('usb') and isinstance(kw['usb'], UsbCommunication):
                    self.communication = kw['usb']
                else:
                    self.communication = UsbCommunication()
            elif kw['comm'] == 'serial':
                if kw.get('serial') and isinstance(kw['serial'], SerialCommunication):
                    self.communication = kw['serial']
                else:
                    self.communication = SerialCommunication()
            else:
                raise ValueError(f"Provided communication type {kw['comm']} is not supported")


    @staticmethod
    def create_message_from(payload: array | tuple | list) -> array:
        message_start_length = 1 + 1  # start byte 0xAA and message length byte
        message_end_length = 1 + 1  # stop bytes 0xD 0xA (CR LF)
        message_length = message_start_length + len(payload) + message_end_length
        message = array('B', message_length * [255])
        message[0] = 0xAA
        message[1] = message_length
        message[2:-2] = array('B', payload)
        message[-2], message[-1] = 0xD, 0xA
        return message

    def send(self, message: array | tuple | list):
        return self.communication.send(message)

    def receive(self):
        return self.communication.receive()

    def send_recv(self, payload: array | tuple | list):
        if self.communication.check_message(payload):
            # valid message was provided already, no need to wrap it further
            message = payload
        else:
            message = BstProtocol.create_message_from(payload)
        return self.communication.send_receive(message)
