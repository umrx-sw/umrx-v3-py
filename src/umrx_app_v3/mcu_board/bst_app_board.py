import inspect
import logging
import struct
from array import array
from dataclasses import dataclass
from typing import Callable, Any, Union

from umrx_app_v3.mcu_board.bst_protocol import BstProtocol

logger = logging.getLogger(__name__)


class AppBoardError(Exception):
    ...


@dataclass
class BoardInfo:
    board_id: int
    hardware_id: int
    software_id: int
    shuttle_id: int


class ApplicationBoard:
    def __init__(self, **kwargs):
        self.protocol: BstProtocol = kwargs['protocol'] if kwargs.get('protocol') else BstProtocol()

    @property
    def board_info(self) -> BoardInfo:
        payload = 2, 31,
        response = self.protocol.send_recv(payload)
        return self.parse_board_info(response)

    def check_message_length(*, expected: int = 0, not_less_then: int = 0) -> Callable:
        def decorator(function: Callable) -> Callable:
            def wrapper(*args: Any, **kwargs: Any) -> Union[None, Any]:
                message = kwargs['message'] if kwargs.get('message') else args[1]
                wrapper.__signature__ = inspect.signature(function)
                if expected and len(message) != expected:
                    logger.error("Expected message length: %s got %s", expected, len(message))
                    logger.error("Check failed, function `%s` will not be executed ", function.__name__)
                    return None
                if not_less_then and len(message) < not_less_then:
                    logger.error("Expect message of length at least %s: got %s", not_less_then, len(message))
                    logger.error("Check failed, function `%s` will not be executed ", function.__name__)
                    return None
                return function(*args, **kwargs)
            return wrapper
        return decorator

    @check_message_length(expected=15)
    def parse_board_info(self, message: array) -> BoardInfo:
        shuttle_id = message[6] << 8 | message[7]
        hardware_id = message[8] << 8 | message[9]
        software_id = message[10] << 8 | message[11]
        board_id = message[12]
        return BoardInfo(board_id=board_id, hardware_id=hardware_id, software_id=software_id, shuttle_id=shuttle_id)

    def switch_app(self, address: int | None = None):
        self.stop_polling_streaming()
        # sleep(0.15)
        self.disable_timer()
        # sleep(0.15)
        self.stop_interrupt_streaming()
        # sleep(0.15)
        address_serialized = (int(a) for a in struct.pack('>L', address))
        payload = 0x01, 0x30, *address_serialized
        ok = self.protocol.send_recv(payload)
        # for _ in range(100):
        #     msg = self.protocol.recv()
        # raise AppBoardError("Switch app failed")
        # self.protocol = UsbCommunication()
        return ok

    def switch_usb_dfu_bl(self):
        return self.switch_app(0)

    def switch_usb_mtp(self):
        return self.switch_app(0x28000)

    def stop_interrupt_streaming(self):
        payload = 0x0A, 0x00
        self.protocol.send_recv(payload)

    def stop_polling_streaming(self):
        payload = 0x06, 0x00
        self.protocol.send_recv(payload)

    def disable_timer(self):
        timer_disable = 0x04
        payload = 0x01, 0x29, timer_disable
        self.protocol.send_recv(payload)
