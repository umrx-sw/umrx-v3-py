import logging
import struct
import time
from array import array
from types import TracebackType
from typing import Any

import usb.core

from umrx_app_v3.mcu_board.comm.comm import Communication
from umrx_app_v3.mcu_board.commands.command import Command

logger = logging.getLogger(__name__)


class UsbCommunicationError(Exception): ...


class UsbCommunication(Communication):
    def __init__(self, **kwargs: Any) -> None:
        self.vid_v3_rev0, self.pid_v3_rev0 = 0x152A, 0x80C0  # default VID/PID for 3.0 HW
        self.vid = kwargs["vid"] if kwargs.get("vid") else self.vid_v3_rev0
        self.pid = kwargs["pid"] if kwargs.get("pid") else self.pid_v3_rev0
        self.usb_device: usb.core.Device | None = None
        self.configuration: usb.core.Configuration | None = None
        self.interface: usb.core.Interface | None = None
        self.endpoint_bulk_in: usb.core.Endpoint | None = None
        self.endpoint_bulk_out: usb.core.Endpoint | None = None
        self.is_initialized = False
        # self.initialize()

    def find_device(self) -> None:
        self.usb_device = usb.core.find(idVendor=self.vid, idProduct=self.pid)
        if self.usb_device is None:
            error_message = f"Board with VID={self.vid:04X}, PID={self.pid:04X} not found! Is it connected and ON?"
            raise UsbCommunicationError(error_message)

    def get_set_usb_config(self) -> None:
        if self.usb_device is None:
            error_message = "USB device is not initialized, cannot continue!"
            raise UsbCommunicationError(error_message)
        if self.vid == self.vid_v3_rev0 and self.pid == self.pid_v3_rev0:
            self.usb_device.set_configuration()
        self.configuration = self.usb_device.get_active_configuration()

    def obtain_endpoints(self) -> None:
        self.interface = self.configuration[(0, 0)]
        if self.vid == self.vid_v3_rev0 and self.pid == self.pid_v3_rev0:
            usb.util.claim_interface(self.usb_device, self.interface.bInterfaceNumber)
        logging.info(f"{self.interface=}")
        if self.usb_device.is_kernel_driver_active(self.interface.bInterfaceNumber):
            self.usb_device.detach_kernel_driver(self.interface.bInterfaceNumber)
            logger.info("Detaching kernel driver done")
        if self.vid == self.vid_v3_rev0 and self.pid == self.pid_v3_rev0:
            self.endpoint_bulk_in = self.interface[0x0]
            logger.info(f"{self.endpoint_bulk_in=}")

            self.endpoint_bulk_out = self.interface[0x1]
            logger.info(f"{self.endpoint_bulk_out=}")

    @property
    def bulk_in_packet_size(self) -> int:
        if not self.endpoint_bulk_in:
            logger.warning("Input endpoint not available!")
            return -1
        return self.endpoint_bulk_in.wMaxPacketSize

    @property
    def bulk_out_packet_size(self) -> int | None:
        if not self.endpoint_bulk_out:
            logger.warning("Output endpoint not available!")
            return None
        return self.endpoint_bulk_out.wMaxPacketSize

    def initialize(self) -> None:
        self.find_device()
        self.get_set_usb_config()
        self.obtain_endpoints()
        self.is_initialized = True

    def connect(self) -> None:
        if not self.is_initialized:
            self.initialize()

    def disconnect(self) -> None:
        pass

    def __enter__(self) -> None:
        self.connect()

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        self.disconnect()

    def send(self, message: array | tuple | list) -> bool:
        if len(message) == 0:
            logger.warning("Nothing to send")
            return False
        packet = self.create_packet_from(message)
        bytes_written = self.endpoint_bulk_out.write(data=packet, timeout=1)
        if bytes_written != len(packet):
            logger.warning(f"Number of bytes written: {bytes_written} != packet length: {len(packet)}")
        return bytes_written == len(packet)

    @staticmethod
    def extract_message_from(packet: array) -> array:
        message_length = packet[1]
        return packet[:message_length]

    def _receive(self) -> array:
        return self.endpoint_bulk_in.read(self.bulk_in_packet_size)

    def receive(self) -> array:
        is_valid_packet_received = False
        packet = None
        reads_done_so_far = 0
        max_num_reads = 64
        while not is_valid_packet_received and reads_done_so_far < max_num_reads:
            packet = self._receive()
            reads_done_so_far += 1
            is_valid_packet_received = Command.check_message(packet)
        return self.extract_message_from(packet)

    def send_receive(self, message: array | tuple | list) -> array:
        self.send(message)
        return self.receive()

    def create_packet_from(self, message: array | tuple | list) -> array:
        if isinstance(message, array) and len(message) == self.bulk_out_packet_size:
            # nothing to do, packet is already in good shape
            return message
        if len(message) > self.bulk_out_packet_size:
            error_message = "Cannot construct packet, the data is too long for USB transfer!"
            raise UsbCommunicationError(error_message)
        packet = array("B", self.bulk_out_packet_size * [255])
        payload = array("B", message)
        packet[0 : len(payload)] = payload
        return packet

    @staticmethod
    def serialize_baud_rate(baud_rate: int) -> tuple[int, ...]:
        return *(int(el) for el in struct.pack("<I", baud_rate)), 0x00, 0x00, 0x08

    def send_control_transfer(self, baud_rate: int) -> None:
        dtr, rts = (1 << 0), (1 << 1)
        payload = self.serialize_baud_rate(baud_rate)
        for _ in range(2):
            self.usb_device.ctrl_transfer(0x21, 0x22, dtr | rts, 0, None)
            self.usb_device.ctrl_transfer(0x21, 0x20, 0, 0, payload)
            self.usb_device.ctrl_transfer(0x21, 0x22, 0, 0, None)
            time.sleep(1)

    def switch_usb_dfu_bl(self) -> None:
        return self.send_control_transfer(1200)

    def switch_usb_mtp(self) -> None:
        return self.send_control_transfer(2400)
