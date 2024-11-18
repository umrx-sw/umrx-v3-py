from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class BMI088:
    gyro_lpm1_addr = 0x11

    def __init__(self) -> None:
        self.read_gyro: Callable | None = None
        self.write_gyro: Callable | None = None

    @property
    def gyro_lpm1(self) -> int:
        return self.read_gyro(BMI088.gyro_lpm1_addr)

    @gyro_lpm1.setter
    def gyro_lpm1(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_lpm1_addr, value)
