import struct
from collections.abc import Callable
from enum import Enum


class BMP585Addr(Enum):
    chip_id = 0x01
    rev_id = 0x02
    chip_status = 0x11
    drive_config = 0x13
    int_config = 0x14
    int_source = 0x15
    fifo_config = 0x16
    fifo_count = 0x17
    fifo_sel = 0x18
    temp_data_xlsb = 0x1D
    temp_data_lsb = 0x1E
    temp_data_msb = 0x1F
    press_data_xlsb = 0x20
    press_data_lsb = 0x21
    press_data_msb = 0x22
    int_status = 0x27
    status = 0x28
    fifo_data = 0x29
    nvm_addr = 0x2B
    nvm_data_lsb = 0x2C
    nvm_data_msb = 0x2D
    dsp_config = 0x30
    dsp_iir = 0x31
    oor_thr_p_lsb = 0x32
    oor_thr_p_msb = 0x33
    oor_range = 0x34
    oor_config = 0x35
    osr_config = 0x36
    odr_config = 0x37
    osr_eff = 0x38
    cmd = 0x7E


class BMP585:
    def __init__(self) -> None:
        self.read: Callable | None = None
        self.write: Callable | None = None

    def assign_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read = read_callback
        self.write = write_callback

    @property
    def chip_id(self) -> int:
        return self.read(BMP585Addr.chip_id)

    @property
    def rev_id(self) -> int:
        return self.read(BMP585Addr.rev_id)

    @property
    def chip_status(self) -> int:
        return self.read(BMP585Addr.chip_status)

    @property
    def drive_config(self) -> int:
        return self.read(BMP585Addr.drive_config)

    @drive_config.setter
    def drive_config(self, value: int) -> None:
        self.write(BMP585Addr.drive_config, value)

    @property
    def int_config(self) -> int:
        return self.read(BMP585Addr.int_config)

    @int_config.setter
    def int_config(self, value: int) -> None:
        self.write(BMP585Addr.int_config, value)

    @property
    def int_source(self) -> int:
        return self.read(BMP585Addr.int_source)

    @int_source.setter
    def int_source(self, value: int) -> None:
        self.write(BMP585Addr.int_source, value)

    @property
    def fifo_config(self) -> int:
        return self.read(BMP585Addr.fifo_config)

    @fifo_config.setter
    def fifo_config(self, value: int) -> None:
        self.write(BMP585Addr.fifo_config, value)

    @property
    def fifo_count(self) -> int:
        return self.read(BMP585Addr.fifo_count)

    @property
    def fifo_sel(self) -> int:
        return self.read(BMP585Addr.fifo_sel)

    @fifo_sel.setter
    def fifo_sel(self, value: int) -> None:
        self.write(BMP585Addr.fifo_sel, value)

    @property
    def temperature(self) -> float:
        xlsb, lsb, msb = self.read(BMP585Addr.temp_data_xlsb, 3)
        (full_degrees,) = struct.unpack("<b", int.to_bytes(msb, 1, byteorder="little"))
        fractional_degrees = ((lsb << 8) | xlsb) / 2**16
        return full_degrees + fractional_degrees

    @property
    def pressure(self) -> float:
        xlsb, lsb, msb = self.read(BMP585Addr.press_data_xlsb, 3)
        return ((msb << 16) | (lsb << 8) | xlsb) / 2**6

    @property
    def int_status(self) -> int:
        return self.read(BMP585Addr.int_status)

    @property
    def status(self) -> int:
        return self.read(BMP585Addr.status)

    @property
    def fifo_data(self) -> int:
        return self.read(BMP585Addr.fifo_data)

    @property
    def nvm_addr(self) -> int:
        return self.read(BMP585Addr.nvm_addr)

    @nvm_addr.setter
    def nvm_addr(self, value: int) -> None:
        self.write(BMP585Addr.nvm_addr, value)

    @property
    def nvm_data_lsb(self) -> int:
        return self.read(BMP585Addr.nvm_data_lsb)

    @nvm_data_lsb.setter
    def nvm_data_lsb(self, value: int) -> None:
        self.write(BMP585Addr.nvm_data_lsb, value)

    @property
    def nvm_data_msb(self) -> int:
        return self.read(BMP585Addr.nvm_data_msb)

    @nvm_data_msb.setter
    def nvm_data_msb(self, value: int) -> None:
        self.write(BMP585Addr.nvm_data_msb, value)

    @property
    def dsp_config(self) -> int:
        return self.read(BMP585Addr.dsp_config)

    @dsp_config.setter
    def dsp_config(self, value: int) -> None:
        self.write(BMP585Addr.dsp_config, value)

    @property
    def dsp_iir(self) -> int:
        return self.read(BMP585Addr.dsp_iir)

    @dsp_iir.setter
    def dsp_iir(self, value: int) -> None:
        self.write(BMP585Addr.dsp_iir, value)

    @property
    def oor_thr_p_lsb(self) -> int:
        return self.read(BMP585Addr.oor_thr_p_lsb)

    @oor_thr_p_lsb.setter
    def oor_thr_p_lsb(self, value: int) -> None:
        self.write(BMP585Addr.oor_thr_p_lsb, value)

    @property
    def oor_thr_p_msb(self) -> int:
        return self.read(BMP585Addr.oor_thr_p_msb)

    @oor_thr_p_msb.setter
    def oor_thr_p_msb(self, value: int) -> None:
        self.write(BMP585Addr.oor_thr_p_msb, value)

    @property
    def oor_range(self) -> int:
        return self.read(BMP585Addr.oor_range)

    @oor_range.setter
    def oor_range(self, value: int) -> None:
        self.write(BMP585Addr.oor_range, value)

    @property
    def oor_config(self) -> int:
        return self.read(BMP585Addr.oor_config)

    @oor_config.setter
    def oor_config(self, value: int) -> None:
        self.write(BMP585Addr.oor_config, value)

    @property
    def osr_config(self) -> int:
        return self.read(BMP585Addr.osr_config)

    @osr_config.setter
    def osr_config(self, value: int) -> None:
        self.write(BMP585Addr.osr_config, value)

    @property
    def odr_config(self) -> int:
        return self.read(BMP585Addr.odr_config)

    @odr_config.setter
    def odr_config(self, value: int) -> None:
        self.write(BMP585Addr.odr_config, value)

    @property
    def osr_eff(self) -> int:
        return self.read(BMP585Addr.osr_eff)

    @property
    def cmd(self) -> int:
        return self.read(BMP585Addr.cmd)

    @cmd.setter
    def cmd(self, value: int) -> None:
        self.write(BMP585Addr.cmd, value)
