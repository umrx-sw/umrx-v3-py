import logging
from array import array
from typing import Any

from umrx_app_v3.mcu_board.bst_app_board import ApplicationBoard
from umrx_app_v3.mcu_board.comm.usb_comm import UsbCommunication
from umrx_app_v3.mcu_board.commands.streaming_polling import StreamingPollingCmd

logger = logging.getLogger(__name__)


class AppBoardV3Rev1Error(Exception): ...


class ApplicationBoardV3Rev1(ApplicationBoard):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, comm="serial")
        self.vid = 0x108C  # App Board 3.1
        self.pid = 0xAB38
        self.usb_comm = UsbCommunication(vid=self.vid, pid=self.pid)

    def switch_usb_dfu_bl(self) -> None:
        return self.usb_comm.switch_usb_dfu_bl()

    def switch_usb_mtp(self) -> None:
        return self.usb_comm.switch_usb_mtp()

    def initialize_usb(self) -> None:
        if not self.usb_comm.is_initialized:
            self.usb_comm.initialize()

    def receive_streaming_multiple(self) -> tuple[int, array[int]]:
        for message in self.protocol.communication.receive_polling_streaming():
            yield StreamingPollingCmd.parse(message)
