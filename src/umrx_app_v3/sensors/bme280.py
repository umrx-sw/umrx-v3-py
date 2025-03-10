import struct
from collections.abc import Callable
from enum import Enum
from functools import cached_property


class BME280Addr(Enum):
    chip_id = 0xD0
    reset = 0xE0
    ctrl_hum = 0xF2
    status = 0xF3
    ctrl_meas = 0xF4
    config = 0xF5
    press_msb = 0xF7
    press_lsb = 0xF8
    press_xlsb = 0xF9
    temp_msb = 0xFA
    temp_lsb = 0xFB
    temp_xlsb = 0xFC
    hum_msb = 0xFD
    hum_lsb = 0xFE


class BME280NVMAddr(Enum):
    dig_t1 = 0x88
    dig_t2 = 0x8A
    dig_t3 = 0x8C
    dig_p1 = 0x8E
    dig_p2 = 0x90
    dig_p3 = 0x92
    dig_p4 = 0x94
    dig_p5 = 0x96
    dig_p6 = 0x98
    dig_p7 = 0x9A
    dig_p8 = 0x9C
    dig_p9 = 0x9E
    dig_h1 = 0xA1
    dig_h2 = 0xE1
    dig_h3 = 0xE3
    dig_h4 = 0xE4
    dig_h5 = 0xE5
    dig_h6 = 0xE7


class BME280:
    def __init__(self) -> None:
        self.read: Callable | None = None
        self.write: Callable | None = None

    def assign_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read = read_callback
        self.write = write_callback

    @property
    def chip_id(self) -> int:
        return self.read(BME280Addr.chip_id)

    def reset(self, value: int) -> None:
        self.write(BME280Addr.reset, value)

    reset = property(None, reset)

    @property
    def ctrl_hum(self) -> int:
        return self.read(BME280Addr.ctrl_hum)

    @ctrl_hum.setter
    def ctrl_hum(self, value: int) -> None:
        self.write(BME280Addr.ctrl_hum, value)

    @property
    def status(self) -> int:
        return self.read(BME280Addr.status)

    @property
    def ctrl_meas(self) -> int:
        return self.read(BME280Addr.ctrl_meas)

    @ctrl_meas.setter
    def ctrl_meas(self, value: int) -> None:
        self.write(BME280Addr.ctrl_meas, value)

    @property
    def config(self) -> int:
        return self.read(BME280Addr.config)

    @config.setter
    def config(self, value: int) -> None:
        self.write(BME280Addr.config, value)

    @property
    def pressure(self) -> int:
        msb, lsb, xlsb = self.read(BME280Addr.press_msb, 3)
        return (msb << 12) | (lsb << 4) | ((xlsb >> 4) & 0x0F)

    @property
    def temperature(self) -> int:
        msb, lsb, xlsb = self.read(BME280Addr.temp_msb, 3)
        return (msb << 12) | (lsb << 4) | ((xlsb >> 4) & 0x0F)

    @property
    def humidity(self) -> int:
        msb, lsb = self.read(BME280Addr.hum_msb, 2)
        return (msb << 8) | lsb

    @cached_property
    def dig_t1(self) -> int:
        payload = self.read(BME280NVMAddr.dig_t1, 2)
        (coefficient,) = struct.unpack("<H", payload)
        return coefficient

    @cached_property
    def dig_t2(self) -> int:
        payload = self.read(BME280NVMAddr.dig_t2, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_t3(self) -> int:
        payload = self.read(BME280NVMAddr.dig_t3, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_p1(self) -> int:
        payload = self.read(BME280NVMAddr.dig_p1, 2)
        (coefficient,) = struct.unpack("<H", payload)
        return coefficient

    @cached_property
    def dig_p2(self) -> int:
        payload = self.read(BME280NVMAddr.dig_p2, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_p3(self) -> int:
        payload = self.read(BME280NVMAddr.dig_p3, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_p4(self) -> int:
        payload = self.read(BME280NVMAddr.dig_p4, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_p5(self) -> int:
        payload = self.read(BME280NVMAddr.dig_p5, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_p6(self) -> int:
        payload = self.read(BME280NVMAddr.dig_p6, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_p7(self) -> int:
        payload = self.read(BME280NVMAddr.dig_p7, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_p8(self) -> int:
        payload = self.read(BME280NVMAddr.dig_p8, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_p9(self) -> int:
        payload = self.read(BME280NVMAddr.dig_p9, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_h1(self) -> int:
        return self.read(BME280NVMAddr.dig_h1)

    @cached_property
    def dig_h2(self) -> int:
        payload = self.read(BME280NVMAddr.dig_h2, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def dig_h3(self) -> int:
        return self.read(BME280NVMAddr.dig_h3)

    @cached_property
    def dig_h4(self) -> int:
        msb, lsb_nibble = self.read(BME280NVMAddr.dig_h4, 2)
        lsb_nibble = lsb_nibble & 0x0F
        sign_part = 0xF0 if (msb >> 7) else 0x00
        value = (sign_part << 8) | (msb << 4) | lsb_nibble
        bytes_payload = bytearray([value >> 8, value & 0xFF])
        (coefficient,) = struct.unpack(">h", bytes_payload)
        return coefficient

    @cached_property
    def dig_h5(self) -> int:
        lsb_nibble, msb = self.read(BME280NVMAddr.dig_h5, 2)
        lsb_nibble = (lsb_nibble & 0xF0) >> 4
        sign_part = 0xF0 if (msb >> 7) else 0x00
        value = (sign_part << 8) | (msb << 4) | lsb_nibble
        bytes_payload = bytearray([value >> 8, value & 0xFF])
        (coefficient,) = struct.unpack(">h", bytes_payload)
        return coefficient

    @cached_property
    def dig_h6(self) -> int:
        payload = self.read(BME280NVMAddr.dig_h6)
        (coefficient,) = struct.unpack("<b", int.to_bytes(payload, 1, byteorder="little"))
        return coefficient

    def compute_t_fine(self, raw_temperature: int) -> float:
        var_1 = (raw_temperature / 16384.0) - self.dig_t1 / 1024.0
        var_1 = var_1 * self.dig_t2
        var_2 = raw_temperature / 131072.0 - (self.dig_t1 / 8192.0)
        var_2 = (var_2**2) * self.dig_t3
        return var_1 + var_2

    def compensate_temperature(self, raw_temperature: int) -> float:
        temperature_min, temperature_max = -40.0, 85.0
        t_fine = self.compute_t_fine(raw_temperature)
        temperature = t_fine / 5120.0
        temperature = max(temperature, temperature_min)
        return min(temperature, temperature_max)

    def compensate_pressure(self, raw_pressure: int, raw_temperature: int) -> float:
        pressure_min, pressure_max = 30000.0, 110000.0
        var_1 = (self.compute_t_fine(raw_temperature) / 2.0) - 64000.0
        var_2 = (var_1**2) * self.dig_p6 / 32768.0
        var_2 = var_2 + var_1 * self.dig_p5 * 2.0
        var_2 = var_2 / 4.0 + self.dig_p4 * 65536.0
        var_3 = self.dig_p3 * var_1 * var_1 / 524288.0
        var_1 = (var_3 + self.dig_p2 * var_1) / 524288.0
        var_1 = (1.0 + var_1 / 32768.0) * self.dig_p1
        if var_1 == 0:
            # invalid case
            return pressure_min
        pressure = 1048576.0 - raw_pressure
        pressure = (pressure - (var_2 / 4096.0)) * 6250.0 / var_1
        var_1 = self.dig_p9 * (pressure**2) / 2147483648.0
        var_2 = pressure * self.dig_p8 / 32768.0
        pressure = pressure + (var_1 + var_2 + self.dig_p7) / 16.0
        pressure = max(pressure, pressure_min)
        return min(pressure, pressure_max)

    def compensate_humidity(self, raw_humidity: int, raw_temperature: int) -> float:
        humidity_min, humidity_max = 0.0, 100.0
        var1 = self.compute_t_fine(raw_temperature) - 76800.0
        var2 = self.dig_h4 * 64.0 + (self.dig_h5 / 16384.0) * var1
        var3 = raw_humidity - var2
        var4 = self.dig_h2 / 65536.0
        var5 = 1.0 + self.dig_h3 / 67108864.0 * var1
        var6 = 1.0 + self.dig_h6 / 67108864.0 * var1 * var5
        var6 = var3 * var4 * var5 * var6
        humidity = var6 * (1.0 - self.dig_h1 * var6 / 524288.0)
        humidity = max(humidity, humidity_min)
        return min(humidity, humidity_max)
