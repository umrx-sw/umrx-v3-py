from dataclasses import dataclass
from math import nan
from typing import ClassVar


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
