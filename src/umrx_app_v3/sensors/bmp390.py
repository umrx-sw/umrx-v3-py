import struct
from collections.abc import Callable
from enum import Enum

from cryptography.utils import cached_property


class BMP390Addr(Enum):
    chip_id = 0x00
    rev_id = 0x01
    err_reg = 0x02
    status = 0x03
    data_0 = 0x04
    data_1 = 0x05
    data_2 = 0x06
    data_3 = 0x07
    data_4 = 0x08
    data_5 = 0x09
    sensor_time_0 = 0x0C
    sensor_time_1 = 0x0D
    sensor_time_2 = 0x0E
    event = 0x10
    int_status = 0x11
    fifo_length_0 = 0x12
    fifo_length_1 = 0x13
    fifo_data = 0x14
    fifo_wtm_0 = 0x15
    fifo_wtm_1 = 0x16
    fifo_config_1 = 0x17
    fifo_config_2 = 0x18
    int_ctrl = 0x19
    int_conf = 0x1A
    pwr_ctrl = 0x1B
    osr = 0x1C
    odr = 0x1D
    config = 0x1F
    cmd = 0x7E


class BMP390NVMAddr(Enum):
    nvm_par_t1 = 0x31
    nvm_par_t2 = 0x33
    nvm_par_t3 = 0x35
    nvm_par_p1 = 0x36
    nvm_par_p2 = 0x38
    nvm_par_p3 = 0x3A
    nvm_par_p4 = 0x3B
    nvm_par_p5 = 0x3C
    nvm_par_p6 = 0x3E
    nvm_par_p7 = 0x40
    nvm_par_p8 = 0x41
    nvm_par_p9 = 0x42
    nvm_par_p10 = 0x44
    nvm_par_p11 = 0x45


class BMP390:
    def __init__(self) -> None:
        self.read: Callable | None = None
        self.write: Callable | None = None

    def assign_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read = read_callback
        self.write = write_callback

    @property
    def chip_id(self) -> int:
        return self.read(BMP390Addr.chip_id)

    @property
    def rev_id(self) -> int:
        return self.read(BMP390Addr.rev_id)

    @property
    def err_reg(self) -> int:
        return self.read(BMP390Addr.err_reg)

    @property
    def status(self) -> int:
        return self.read(BMP390Addr.status)

    @property
    def pressure(self) -> int:
        byte_0, byte_1, byte_2 = self.read(BMP390Addr.data_0, 3)
        return (byte_2 << 16) | (byte_1 << 8) | byte_0

    @property
    def temperature(self) -> int:
        byte_0, byte_1, byte_2 = self.read(BMP390Addr.data_3, 3)
        return (byte_2 << 16) | (byte_1 << 8) | byte_0

    @property
    def sensor_time(self) -> int:
        byte_0, byte_1, byte_2 = self.read(BMP390Addr.sensor_time_0, 3)
        return (byte_2 << 16) | (byte_1 << 8) | byte_0

    @property
    def event(self) -> int:
        return self.read(BMP390Addr.event)

    @property
    def int_status(self) -> int:
        return self.read(BMP390Addr.int_status)

    @property
    def fifo_length(self) -> int:
        # TODO: interpret the payload
        return self.read(BMP390Addr.fifo_length_0, 2)

    @property
    def fifo_data(self) -> int:
        return self.read(BMP390Addr.fifo_data)

    @property
    def fifo_wtm_0(self) -> int:
        return self.read(BMP390Addr.fifo_wtm_0)

    @fifo_wtm_0.setter
    def fifo_wtm_0(self, value: int) -> None:
        self.write(BMP390Addr.fifo_wtm_0, value)

    @property
    def fifo_wtm_1(self) -> int:
        return self.read(BMP390Addr.fifo_wtm_1)

    @fifo_wtm_1.setter
    def fifo_wtm_1(self, value: int) -> None:
        self.write(BMP390Addr.fifo_wtm_1, value)

    @property
    def fifo_config_1(self) -> int:
        return self.read(BMP390Addr.fifo_config_1)

    @fifo_config_1.setter
    def fifo_config_1(self, value: int) -> None:
        self.write(BMP390Addr.fifo_config_1, value)

    @property
    def fifo_config_2(self) -> int:
        return self.read(BMP390Addr.fifo_config_2)

    @fifo_config_2.setter
    def fifo_config_2(self, value: int) -> None:
        self.write(BMP390Addr.fifo_config_2, value)

    @property
    def int_ctrl(self) -> int:
        return self.read(BMP390Addr.int_ctrl)

    @int_ctrl.setter
    def int_ctrl(self, value: int) -> None:
        self.write(BMP390Addr.int_ctrl, value)

    @property
    def int_conf(self) -> int:
        return self.read(BMP390Addr.int_conf)

    @int_conf.setter
    def int_conf(self, value: int) -> None:
        self.write(BMP390Addr.int_conf, value)

    @property
    def pwr_ctrl(self) -> int:
        return self.read(BMP390Addr.pwr_ctrl)

    @pwr_ctrl.setter
    def pwr_ctrl(self, value: int) -> None:
        self.write(BMP390Addr.pwr_ctrl, value)

    @property
    def osr(self) -> int:
        return self.read(BMP390Addr.osr)

    @osr.setter
    def osr(self, value: int) -> None:
        self.write(BMP390Addr.osr, value)

    @property
    def odr(self) -> int:
        return self.read(BMP390Addr.odr)

    @odr.setter
    def odr(self, value: int) -> None:
        self.write(BMP390Addr.odr, value)

    @property
    def config(self) -> int:
        return self.read(BMP390Addr.config)

    @config.setter
    def config(self, value: int) -> None:
        self.write(BMP390Addr.config, value)

    @property
    def cmd(self) -> int:
        return self.read(BMP390Addr.cmd)

    @cmd.setter
    def cmd(self, value: int) -> None:
        self.write(BMP390Addr.cmd, value)

    @cached_property
    def nvm_par_t1(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_t1, 2)
        (coefficient,) = struct.unpack("<H", payload)
        return coefficient

    @cached_property
    def nvm_par_t2(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_t2, 2)
        (coefficient,) = struct.unpack("<H", payload)
        return coefficient

    @cached_property
    def nvm_par_t3(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_t3)
        (coefficient,) = struct.unpack("<b", int.to_bytes(payload, 1, byteorder="little"))
        return coefficient

    @cached_property
    def nvm_par_p1(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p1, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def nvm_par_p2(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p2, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def nvm_par_p3(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p3)
        (coefficient,) = struct.unpack("<b", int.to_bytes(payload, 1, byteorder="little"))
        return coefficient

    @cached_property
    def nvm_par_p4(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p4)
        (coefficient,) = struct.unpack("<b", int.to_bytes(payload, 1, byteorder="little"))
        return coefficient

    @cached_property
    def nvm_par_p5(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p5, 2)
        (coefficient,) = struct.unpack("<H", payload)
        return coefficient

    @cached_property
    def nvm_par_p6(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p6, 2)
        (coefficient,) = struct.unpack("<H", payload)
        return coefficient

    @cached_property
    def nvm_par_p7(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p7)
        (coefficient,) = struct.unpack("<b", int.to_bytes(payload, 1, byteorder="little"))
        return coefficient

    @cached_property
    def nvm_par_p8(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p8)
        (coefficient,) = struct.unpack("<b", int.to_bytes(payload, 1, byteorder="little"))
        return coefficient

    @cached_property
    def nvm_par_p9(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p9, 2)
        (coefficient,) = struct.unpack("<h", payload)
        return coefficient

    @cached_property
    def nvm_par_p10(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p10)
        (coefficient,) = struct.unpack("<b", int.to_bytes(payload, 1, byteorder="little"))
        return coefficient

    @cached_property
    def nvm_par_p11(self) -> int:
        payload = self.read(BMP390NVMAddr.nvm_par_p11)
        (coefficient,) = struct.unpack("<b", int.to_bytes(payload, 1, byteorder="little"))
        return coefficient

    @cached_property
    def par_t1(self) -> float:
        return self.nvm_par_t1 / (2**-8)

    @cached_property
    def par_t2(self) -> float:
        return self.nvm_par_t2 / (2**30)

    @cached_property
    def par_t3(self) -> float:
        return self.nvm_par_t3 / (2**48)

    @cached_property
    def par_p1(self) -> float:
        return (self.nvm_par_p1 - 2**14) / (2**20)

    @cached_property
    def par_p2(self) -> float:
        return (self.nvm_par_p2 - 2**14) / (2**29)

    @cached_property
    def par_p3(self) -> float:
        return self.nvm_par_p3 / (2**32)

    @cached_property
    def par_p4(self) -> float:
        return self.nvm_par_p4 / (2**37)

    @cached_property
    def par_p5(self) -> float:
        return self.nvm_par_p5 / (2**-3)

    @cached_property
    def par_p6(self) -> float:
        return self.nvm_par_p6 / (2**6)

    @cached_property
    def par_p7(self) -> float:
        return self.nvm_par_p7 / (2**8)

    @cached_property
    def par_p8(self) -> float:
        return self.nvm_par_p8 / (2**15)

    @cached_property
    def par_p9(self) -> float:
        return self.nvm_par_p9 / (2**48)

    @cached_property
    def par_p10(self) -> float:
        return self.nvm_par_p10 / (2**48)

    @cached_property
    def par_p11(self) -> float:
        return self.nvm_par_p11 / (2**65)

    def compensate_temperature(self, raw_temperature: int) -> float:
        p_data1 = raw_temperature - self.par_t1
        p_data2 = p_data1 * self.par_t2
        return p_data2 + (p_data1**2) * self.par_t3

    def compensate_pressure(self, raw_pressure: int, compensated_temperature: float) -> float:
        p_out1 = (
            self.par_p5
            + self.par_p6 * compensated_temperature
            + self.par_p7 * (compensated_temperature**2)
            + self.par_p8 * (compensated_temperature**3)
        )

        p_out2 = raw_pressure * (
            self.par_p1
            + self.par_p2 * compensated_temperature
            + self.par_p3 * (compensated_temperature**2)
            + self.par_p4 * (compensated_temperature**3)
        )

        p_data4 = (self.par_p9 + self.par_p10 * compensated_temperature) * (raw_pressure**2) + self.par_p11 * (
            raw_pressure**3
        )

        return p_out1 + p_out2 + p_data4
