import abc
from array import array
from typing import Any


class Communication(abc.ABC):
    @abc.abstractmethod
    def send(self, message: Any) -> bool: ...

    @abc.abstractmethod
    def receive(self) -> Any: ...

    @abc.abstractmethod
    def send_receive(self, message: Any) -> Any: ...

    @abc.abstractmethod
    def find_device(self) -> None: ...

    @abc.abstractmethod
    def initialize(self) -> None: ...

    @abc.abstractmethod
    def connect(self) -> None: ...

    @abc.abstractmethod
    def disconnect(self) -> None: ...

    @staticmethod
    def check_message(packet: list[int] | array[int] | tuple[int, ...]) -> bool:
        packet_start = 0xAA
        is_packet_start_found = packet[0] == packet_start
        packet_size = packet[1]
        packet_end = 0x0D, 0x0A
        is_packet_end_found = tuple(packet[packet_size - 2 : packet_size]) == packet_end
        return is_packet_start_found and is_packet_end_found
