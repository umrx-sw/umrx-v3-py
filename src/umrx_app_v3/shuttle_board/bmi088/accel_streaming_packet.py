from dataclasses import dataclass
from math import nan
from typing import ClassVar


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
