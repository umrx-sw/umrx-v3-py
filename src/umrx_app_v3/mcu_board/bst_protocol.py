#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT


import logging
from array import array
from typing import List, Tuple, Union

from src.umrx_app_v3.mcu_board import UsbCommunication


class BstProtocol:
    def __init__(self, *a, **kw):
        self.usb: UsbCommunication = kw['usb'] if kw.get('usb') else UsbCommunication()

    @staticmethod
    def check_message(packet: array):
        packet_start = 0xAA
        is_packet_start_found = packet[0] == packet_start
        packet_size = packet[1]
        packet_end = 0x0D, 0x0A
        is_packet_end_found = tuple(packet[packet_size-2:packet_size]) == packet_end
        return is_packet_start_found and is_packet_end_found

    @staticmethod
    def extract_message_from(packet: array) -> array:
        message_length = packet[1]
        return packet[:message_length]

    @staticmethod
    def create_message_from(payload: Union[array, Tuple, List]) -> array:
        message_start_length = 1 + 1  # start byte 0xAA and message length byte
        message_end_length = 1 + 1  # stop bytes 0xD 0xA (CR LF)
        message_length = message_start_length + len(payload) + message_end_length
        message = array('B', message_length * [255])
        message[0] = 0xAA
        message[1] = message_length
        message[2:-2] = array('B', payload)
        message[-2], message[-1] = 0xD, 0xA
        return message

    def send(self, message: Union[array, Tuple, List]):
        return self.usb.send(message)

    def recv(self, max_num_reads=64) -> array:
        is_valid_packet_received = False
        packet = None
        reads_done_so_far = 0
        while not is_valid_packet_received and reads_done_so_far < max_num_reads:
            packet = self.usb.recv()
            reads_done_so_far += 1
            is_valid_packet_received = BstProtocol.check_message(packet)
            logging.debug(f"[recv] num reads made: {reads_done_so_far}")
        return self.extract_message_from(packet)

    def send_recv(self, payload: Union[array, Tuple, List]):
        if BstProtocol.check_message(payload):
            # valid message was provided already, no need to wrap it further
            message = payload
        else:
            message = BstProtocol.create_message_from(payload)
        self.send(message)
        return self.recv()
