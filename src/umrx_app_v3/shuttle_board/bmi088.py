import json
import logging
import struct
from array import array
from collections.abc import Callable, Generator
from dataclasses import dataclass
from math import nan
from pathlib import Path
from typing import Any, ClassVar, Self

from umrx_app_v3.mcu_board.app_board_v3_rev0 import ApplicationBoardV3Rev0
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_app_board import ApplicationBoard

logger = logging.getLogger(__name__)


class BMI088Error(Exception): ...


@dataclass
class BMI088GyroPacket:
    g_x_raw: int
    g_y_raw: int
    g_z_raw: int
    g_x: float = nan
    g_y: float = nan
    g_z: float = nan
    resolution: ClassVar[float] = 2000.0

    def __post_init__(self) -> None:
        self.apply_resolution()

    def apply_resolution(self) -> None:
        self.g_x = self.g_x_raw / BMI088GyroPacket.resolution
        self.g_y = self.g_y_raw / BMI088GyroPacket.resolution
        self.g_z = self.g_z_raw / BMI088GyroPacket.resolution

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"g=[{self.g_x:>+8.3f}; {self.g_y:>+8.3f}; {self.g_z:>+8.3f}]; "
            f"g_raw=[{self.g_x_raw:>+8d}; {self.g_y_raw:>+8d}; {self.g_z_raw:>+8d}]; "
            f"resolution={BMI088GyroPacket.resolution:>6.2f})"
        )

    def to_csv(self) -> str:
        return (
            f"{self.g_x:>+8.3f};{self.g_y:>+8.3f};{self.g_z:>+8.3f};"
            f"{self.g_x_raw:>+8d};{self.g_y_raw:>+8d};{self.g_z_raw:>+8d};\n"
        )

    @staticmethod
    def csv_header() -> str:
        return f"g_x;g_y;g_z;g_x_raw;g_y_raw;g_z_raw;resolution={BMI088GyroPacket.resolution};\n"


@dataclass
class BMI088AccelPacket:
    a_x_raw: int
    a_y_raw: int
    a_z_raw: int
    a_x: float = nan
    a_y: float = nan
    a_z: float = nan
    resolution: ClassVar[float] = 16.0

    def __post_init__(self) -> None:
        self.apply_resolution()

    def apply_resolution(self) -> None:
        self.a_x = self.a_x_raw / BMI088AccelPacket.resolution
        self.a_y = self.a_y_raw / BMI088AccelPacket.resolution
        self.a_z = self.a_z_raw / BMI088AccelPacket.resolution

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"a=[{self.a_x:>+8.3f}; {self.a_y:>+8.3f}; {self.a_z:>+8.3f}]; "
            f"a_raw=[{self.a_x_raw:>+8d}; {self.a_y_raw:>+8d}; {self.a_z_raw:>+8d}]; "
            f"resolution={self.resolution:>6.2f})"
        )

    def to_csv(self) -> str:
        return (
            f"{self.a_x:>+8.3f};{self.a_y:>+8.3f};{self.a_z:>+8.3f};"
            f"{self.a_x_raw:>+8d};{self.a_y_raw:>+8d};{self.a_z_raw:>+8d};\n"
        )

    @staticmethod
    def csv_header() -> str:
        return f"a_x;a_y;a_z;a_x_raw;a_y_raw;a_z_raw;resolution={BMI088AccelPacket.resolution};\n"


class BMI088:
    def __init__(self, **kw: Any) -> None:
        self.file_path = Path(__file__)
        self.command_file = self.file_path.parent / "bmi088_commands.json"
        self.commands = None
        self.board: ApplicationBoard | None = kw["board"] if kw.get("board") else None
        self.parse_commands()

    def attach_to(self, board: ApplicationBoard) -> None:
        self.board = board

    @classmethod
    def create_instance_for_v3_rev0(cls) -> Self:
        board = ApplicationBoardV3Rev0()
        return BMI088(board=board)

    @classmethod
    def create_instance_for_v3_rev1(cls) -> Self:
        board = ApplicationBoardV3Rev1()
        return BMI088(board=board)

    def parse_commands(self) -> None:
        assert self.command_file.exists(), f"Cannot find the {self.command_file}!"
        with Path.open(self.command_file) as fd:
            self.commands = json.load(fd)

    def init(self) -> None:
        commands = self.commands["init"]
        self.send_recv_commands(commands, log_str="[BMI088_INIT]")

    def start_broadcast(self) -> None:
        commands = self.commands["start_broadcast"]
        self.send_recv_commands(commands, log_str="[BMI088_START_BROADCAST]")

    def stop_broadcast(self) -> None:
        commands = self.commands["stop_broadcast"]
        self.send_recv_commands(commands, log_str="[BMI088_START_BROADCAST]")

    def read_register(self) -> None:
        commands = self.commands["read_register"]
        self.send_recv_commands(commands, log_str="[BMI088_READ_REG]")

    def write_register(self) -> None:
        commands = self.commands["write_register"]
        self.send_recv_commands(commands, log_str="[BMI088_WRITE_REG]")

    def receive_broadcast(self, num_packets: int = -1) -> Generator[BMI088GyroPacket | BMI088AccelPacket]:
        received_packets = 0
        logging.getLogger().setLevel(logging.INFO)
        while num_packets == -1 or received_packets < num_packets:
            response = self.board.protocol.receive()
            yield self.decode(response)
            # logging.info(f"[BMI088_BROADCAST]: {response=}")
            received_packets += 1

    def receive_specific_broadcast_packets(
        self, predicate: Callable, interpret: Callable, num_packets: int = -1
    ) -> Generator[BMI088GyroPacket | BMI088AccelPacket]:
        received_packets = 0
        logging.getLogger().setLevel(logging.INFO)
        while num_packets == -1 or received_packets < num_packets:
            response = self.board.protocol.receive()
            if predicate(response):
                yield interpret(response)
                received_packets += 1

    def receive_gyro_broadcast(self, num_packets: int = -1) -> Generator[BMI088GyroPacket]:
        return self.receive_specific_broadcast_packets(self.is_gyro_broadcast, self.decode_gyro_broadcast, num_packets)

    def receive_accel_broadcast(self, num_packets: int = -1) -> Generator[BMI088AccelPacket]:
        return self.receive_specific_broadcast_packets(
            self.is_accel_broadcast, self.decode_accel_broadcast, num_packets
        )

    def decode(self, packet: array[int]) -> BMI088GyroPacket | BMI088AccelPacket:
        if self.is_gyro_broadcast(packet):
            return self.decode_gyro_broadcast(packet)
        if self.is_accel_broadcast(packet):
            return self.decode_accel_broadcast(packet)
        error_message = f"{packet} is of unknown type, neither gyro nor accel"
        raise BMI088Error(error_message)

    @staticmethod
    def is_gyro_broadcast(packet: array[int]) -> bool:
        expected_packet_length = 18
        return len(packet) == expected_packet_length

    @staticmethod
    def is_accel_broadcast(packet: array[int]) -> bool:
        expected_packet_length = 26
        return len(packet) == expected_packet_length

    @staticmethod
    def check_broadcast(func: Callable[..., array[int]]) -> Callable[..., array[int]]:
        def inner(self: Self, packet: array) -> Any:
            if packet[4] != 135:
                logging.info("[ERROR] in broadcast!")
            return func(self, packet)

        return inner

    @check_broadcast
    def decode_gyro_broadcast(self, packet: array[int]) -> BMI088GyroPacket:
        x_raw, y_raw, z_raw = struct.unpack("<hhh", packet[5:11])
        return BMI088GyroPacket(g_x_raw=x_raw, g_y_raw=y_raw, g_z_raw=z_raw)

    @check_broadcast
    def decode_accel_broadcast(self, packet: array[int]) -> BMI088AccelPacket:
        x_raw, y_raw, z_raw = struct.unpack("<hhh", packet[6:12])
        return BMI088AccelPacket(a_x_raw=x_raw, a_y_raw=y_raw, a_z_raw=z_raw)

    def send_recv_commands(self, command_list: list, log_str: str = "") -> None:
        for command in command_list:
            logger.info(f"{command=}")
            init_command_array = array("B", command)
            self.board.protocol.send(init_command_array)
            response = self.board.protocol.receive()
            logger.info(f"{log_str}: {response=}")

    def read_gyro_register_spi(self, reg_addr: int) -> None:
        device_address = 0
        num_of_bytes_to_read = 1
        payload = (
            2,
            22,
            2,
            3,
            3,
            1,
            (device_address >> 8) & 0xFF,
            device_address & 0xFF,
            reg_addr & 0xFF,
            (num_of_bytes_to_read >> 8) & 0xFF,
            num_of_bytes_to_read & 0xFF,
            1,
            0,
            1,
        )
        response = self.board.protocol.send_receive(payload)
        logger.info(response)

    def read_accel_register_spi(self, reg_addr: int) -> None:
        """Read over SPI.

        170, 18, 2, 22, 1, 7, 1, 1, 0, 0, 2, 0, 2, 1, 0, 1, 13, 10,
        170, 18, 2, 22, 1, 7, 1, 1, 0, 0, 1, 0, 2, 1, 0, 1, 13, 10,
        :param reg_addr:
        :return:
        """
        device_address = 0
        num_of_bytes_to_read = 2
        payload = (
            2,
            22,
            1,
            7,
            1,
            1,
            (device_address >> 8) & 0xFF,
            device_address & 0xFF,
            reg_addr & 0xFF,
            (num_of_bytes_to_read >> 8) & 0xFF,
            num_of_bytes_to_read & 0xFF,
            1,
            0,
            1,
        )
        response = self.board.protocol.send_receive(payload)
        logger.info(response)


if __name__ == "__main__":
    """ See `examples` for how to use the shuttle board"""
