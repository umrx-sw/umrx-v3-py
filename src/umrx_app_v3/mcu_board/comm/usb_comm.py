import logging
from array import array

import usb.core

from umrx_app_v3.mcu_board.comm.comm import Communication

logger = logging.getLogger(__name__)


class UsbCommunicationError(Exception):
    ...


class UsbCommunication(Communication):
    def __init__(self, *a, **kw):
        self.vid = 0x152a
        self.pid = 0x80c0
        self.usb_device: usb.core.Device | None = None
        self.configuration: usb.core.Configuration | None = None
        self.interface: usb.core.Interface | None = None
        self.endpoint_bulk_in: usb.core.Endpoint | None = None
        self.endpoint_bulk_out: usb.core.Endpoint | None = None
        self.is_initialized = False
        # self.initialize()

    def find_device(self):
        self.usb_device = usb.core.find(idVendor=self.vid, idProduct=self.pid)
        if self.usb_device is None:
            raise UsbCommunicationError(f"BST Board with VID={self.vid}, PID={self.pid} not connected!"
                                    " Did you plug in the board to PC and turn it ON?")

    def get_set_usb_config(self):
        self.usb_device.set_configuration()
        self.configuration = self.usb_device.get_active_configuration()

    def obtain_endpoints(self):
        self.interface = self.configuration[(0, 0)]
        usb.util.claim_interface(self.usb_device, self.interface.bInterfaceNumber)
        logging.info(f"{self.interface=}")
        if self.usb_device.is_kernel_driver_active(self.interface.bInterfaceNumber):
            self.usb_device.detach_kernel_driver(self.interface.bInterfaceNumber)
            logger.info("Detaching kernel driver done")

        self.endpoint_bulk_in = self.interface[0x0]
        logger.info(f"{self.endpoint_bulk_in=}")

        self.endpoint_bulk_out = self.interface[0x1]
        logger.info(f"{self.endpoint_bulk_out=}")


    @property
    def bulk_in_packet_size(self):
        if not self.endpoint_bulk_in:
            logger.warning("Input endpoint not available!")
            return -1
        return self.endpoint_bulk_in.wMaxPacketSize

    @property
    def bulk_out_packet_size(self):
        if not self.endpoint_bulk_out:
            logger.warning("Output endpoint not available!")
            return None
        return self.endpoint_bulk_out.wMaxPacketSize

    def initialize(self):
        self.find_device()
        self.get_set_usb_config()
        self.obtain_endpoints()
        self.is_initialized = True

    def connect(self):
        if not self.is_initialized:
            self.initialize()

    def disconnect(self):
        pass

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def send(self, message: array | tuple | list) -> bool:
        if len(message) == 0:
            logger.warning("Nothing to send")
            return False
        packet = self.create_packet_from(message)
        bytes_written = self.endpoint_bulk_out.write(data=packet, timeout=1)
        logging.debug(f"{bytes_written=}")
        if bytes_written != len(packet):
            logger.warning(f"Number of bytes written: {bytes_written} != packet length: {len(packet)}")
        return bytes_written == len(packet)

    def _receive(self) -> array:
        data_recv = self.endpoint_bulk_in.read(self.bulk_in_packet_size)
        logging.debug(f"{data_recv}")
        return data_recv

    @staticmethod
    def extract_message_from(packet: array) -> array:
        message_length = packet[1]
        return packet[:message_length]

    def receive(self) -> array:
        is_valid_packet_received = False
        packet = None
        reads_done_so_far = 0
        max_num_reads = 64
        while not is_valid_packet_received and reads_done_so_far < max_num_reads:
            packet = self._receive()
            reads_done_so_far += 1
            is_valid_packet_received = self.check_message(packet)
            logger.debug(f"[recv] num reads made: {reads_done_so_far}")
        return self.extract_message_from(packet)

    def create_packet_from(self, message: array | tuple | list) -> array:
        if isinstance(message, array) and len(message) == self.bulk_out_packet_size:
            # nothing to do, packet is already in good shape
            return message
        if len(message) > self.bulk_out_packet_size:
            raise UsbCommunicationError("Cannot construct packet, the data is too long for USB transfer!")
        packet = array("B", self.bulk_out_packet_size * [255])
        payload = array("B", message)
        packet[0:len(payload)] = payload
        return packet

    def send_receive(self, message):
        self.send(message)
        return self.receive()
