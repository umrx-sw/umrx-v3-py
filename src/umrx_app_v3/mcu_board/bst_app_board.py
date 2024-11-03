import logging
import time
from typing import Any

from umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from umrx_app_v3.mcu_board.commands.app_switch import AppSwitchCmd
from umrx_app_v3.mcu_board.commands.board_info import BoardInfo, BoardInfoCmd
from umrx_app_v3.mcu_board.commands.set_vdd_vddio import SetVddVddioCmd
from umrx_app_v3.mcu_board.commands.streaming import StopInterruptStreamingCmd, StopPollingStreamingCmd
from umrx_app_v3.mcu_board.commands.timer import StopTimerCmd

logger = logging.getLogger(__name__)


class AppBoardError(Exception): ...


class ApplicationBoard:
    def __init__(self, **kw: Any) -> None:
        self.protocol: BstProtocol = (
            kw["protocol"] if kw.get("protocol") and isinstance(kw["protocol"], BstProtocol) else BstProtocol(kw)
        )

    @property
    def board_info(self) -> BoardInfo:
        cmd = BoardInfoCmd.assemble()
        response = self.protocol.send_receive(cmd)
        return BoardInfoCmd.parse(response)

    def set_vdd_vddio(self, vdd: float, vddio: float) -> None:
        payload = SetVddVddioCmd.assemble(vdd, vddio)
        self.protocol.send_receive(payload)

    def switch_app(self, address: int = 0) -> None:
        payload = AppSwitchCmd.assemble(address)
        self.protocol.send_receive(payload)

    def start_communication(self) -> None:
        self.stop_polling_streaming()
        time.sleep(0.15)
        self.disable_timer()
        time.sleep(0.15)
        self.stop_interrupt_streaming()
        time.sleep(0.15)

    def switch_usb_dfu_bl(self) -> None:
        self.start_communication()
        return self.switch_app(0)

    def switch_usb_mtp(self) -> None:
        self.start_communication()
        return self.switch_app(0x28000)

    def stop_interrupt_streaming(self) -> None:
        payload = StopInterruptStreamingCmd.assemble()
        self.protocol.send_receive(payload)

    def stop_polling_streaming(self) -> None:
        payload = StopPollingStreamingCmd.assemble()
        self.protocol.send_receive(payload)

    def disable_timer(self) -> None:
        payload = StopTimerCmd.assemble()
        self.protocol.send_receive(payload)
