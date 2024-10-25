import logging
import usb.core
from array import array
from typing import Union, Tuple, List


class BstBoardException(Exception):
    pass


class UsbCommunication:
    def __init__(self, *a, **kw):
        self.vid = 0x152a
        self.pid = 0x80c0
        self.usb_device: Union[usb.core.Device, None] = None
        self.configuration: Union[usb.core.Configuration, None] = None
        self.interface: Union[usb.core.Interface, None] = None
        self.endpoint_bulk_in: Union[usb.core.Endpoint, None] = None
        self.endpoint_bulk_out: Union[usb.core.Endpoint, None] = None
        self.is_initialized = False
        self.init_usb_comm()

    def find_usb_device(self):
        self.usb_device = usb.core.find(idVendor=self.vid, idProduct=self.pid)
        if self.usb_device is None:
            raise BstBoardException(f'BST Board with VID={self.vid}, PID={self.pid} not connected!'
                                    ' Did you plug in the board to PC and turn it ON?')

    def get_set_usb_config(self):
        self.usb_device.set_configuration()
        self.configuration = self.usb_device.get_active_configuration()

    def obtain_endpoints(self):
        self.interface = self.configuration[(0, 0)]
        usb.util.claim_interface(self.usb_device, self.interface.bInterfaceNumber)
        logging.info(f"{self.interface=}")
        if self.usb_device.is_kernel_driver_active(self.interface.bInterfaceNumber):
            self.usb_device.detach_kernel_driver(self.interface.bInterfaceNumber)
            logging.info(f"Detaching kernel driver done")

        self.endpoint_bulk_in = self.interface[0x0]
        logging.info(f"{self.endpoint_bulk_in=}")

        self.endpoint_bulk_out = self.interface[0x1]
        logging.info(f"{self.endpoint_bulk_out=}")
        self.is_initialized = True

    @property
    def bulk_in_packet_size(self):
        if not self.endpoint_bulk_in:
            logging.warning(f"Input endpoint not available!")
            return
        return self.endpoint_bulk_in.wMaxPacketSize

    @property
    def bulk_out_packet_size(self):
        if not self.endpoint_bulk_out:
            logging.warning(f"Output endpoint not available!")
            return
        return self.endpoint_bulk_out.wMaxPacketSize

    def init_usb_comm(self):
        self.find_usb_device()
        self.get_set_usb_config()
        self.obtain_endpoints()

    def connect(self):
        if not self.is_initialized:
            self.init_usb_comm()

    def disconnect(self):
        pass

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def send(self, message: Union[array, Tuple, List]) -> bool:
        if len(message) == 0:
            logging.warning("Nothing to send")
            return False
        packet = self.create_packet_from(message)
        bytes_written = self.endpoint_bulk_out.write(data=packet)
        logging.debug(f"{bytes_written=}")
        if bytes_written != len(packet):
            logging.warning(f"Number of bytes written: {bytes_written} != packet length: {len(packet)}")
        return bytes_written == len(packet)

    def recv(self) -> array:
        data_recv = self.endpoint_bulk_in.read(self.bulk_in_packet_size)
        logging.debug(f"{data_recv}")
        return data_recv

    def create_packet_from(self, message: Union[Tuple, List, array]) -> array:
        if isinstance(message, array) and len(message) == self.bulk_out_packet_size:
            # nothing to do, packet is already in good shape
            return message
        if len(message) > self.bulk_out_packet_size:
            raise BstBoardException("Cannot construct packet, the data is too long for USB transfer!")
        packet = array('B', self.bulk_out_packet_size * [255])
        payload = array('B', message)
        packet[0:len(payload)] = payload
        return packet
