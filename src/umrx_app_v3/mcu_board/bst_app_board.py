import logging
import time
from array import array
from typing import Any

from umrx_app_v3.mcu_board.bst_protocol import BstProtocol
from umrx_app_v3.mcu_board.bst_protocol_constants import I2CMode, MultiIOPin, PinDirection, PinValue, SPISpeed
from umrx_app_v3.mcu_board.commands.app_switch import AppSwitchCmd
from umrx_app_v3.mcu_board.commands.board_info import BoardInfo, BoardInfoCmd
from umrx_app_v3.mcu_board.commands.i2c import I2CConfigureCmd, I2CReadCmd, I2CWriteCmd
from umrx_app_v3.mcu_board.commands.pin_config import GetPinConfigCmd, SetPinConfigCmd
from umrx_app_v3.mcu_board.commands.set_vdd_vddio import SetVddVddioCmd, Volts
from umrx_app_v3.mcu_board.commands.spi import SPIConfigureCmd, SPIReadCmd
from umrx_app_v3.mcu_board.commands.streaming import StopInterruptStreamingCmd, StopPollingStreamingCmd
from umrx_app_v3.mcu_board.commands.timer import StopTimerCmd

logger = logging.getLogger(__name__)


class AppBoardError(Exception): ...


class ApplicationBoard:
    def __init__(self, **kw: Any) -> None:
        self.protocol: BstProtocol = (
            kw["protocol"] if kw.get("protocol") and isinstance(kw["protocol"], BstProtocol) else BstProtocol(kw)
        )

    def initialize(self) -> None:
        self.protocol.initialize()

    @property
    def board_info(self) -> BoardInfo:
        cmd = BoardInfoCmd.assemble()
        response = self.protocol.send_receive(cmd)
        return BoardInfoCmd.parse(response)

    def set_vdd_vddio(self, vdd: Volts, vddio: Volts) -> None:
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

    def configure_i2c(self, mode: I2CMode = I2CMode.STANDARD_MODE) -> None:
        for payload in I2CConfigureCmd.assemble(mode):
            self.protocol.send_receive(payload)

    def read_i2c(self, i2c_address: int, register_address: int, bytes_to_read: int) -> array[int]:
        payload = I2CReadCmd.assemble(
            i2c_address=i2c_address, register_address=register_address, bytes_to_read=bytes_to_read
        )
        response = self.protocol.send_receive(payload)
        return I2CReadCmd.parse(response)

    def write_i2c(self, i2c_address: int, start_register_address: int, data_to_write: array[int]) -> None:
        payload = I2CWriteCmd.assemble(
            i2c_address=i2c_address, start_register_address=start_register_address, data_to_write=data_to_write
        )
        self.protocol.send_receive(payload)

    def set_pin_config(self, pin: MultiIOPin, direction: PinDirection, value: PinValue) -> None:
        payload = SetPinConfigCmd.assemble(pin=pin, direction=direction, value=value)
        self.protocol.send_receive(payload)

    def get_pin_config(self, pin: MultiIOPin) -> tuple[PinDirection, PinValue]:
        payload = GetPinConfigCmd.assemble(pin=pin)
        response = self.protocol.send_receive(payload)
        return GetPinConfigCmd.parse(response)

    def configure_spi(self, speed: SPISpeed = SPISpeed.MHz_5) -> None:
        for payload in SPIConfigureCmd.assemble(speed):
            self.protocol.send_receive(payload)

    def read_spi(self, cs_pin: MultiIOPin, register_address: int, bytes_to_read: int) -> array[int]:
        payload = SPIReadCmd.assemble(cs_pin=cs_pin, register_address=register_address, bytes_to_read=bytes_to_read)
        response = self.protocol.send_receive(payload)
        return SPIReadCmd.parse(response)
