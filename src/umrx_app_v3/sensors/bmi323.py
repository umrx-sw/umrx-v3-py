import struct
from collections.abc import Callable
from enum import Enum


class BMI323Addr(Enum):
    chip_id = 0x00
    err_reg = 0x01
    status = 0x02
    acc_data_x = 0x03
    acc_data_y = 0x04
    acc_data_z = 0x05
    gyr_data_x = 0x06
    gyr_data_y = 0x07
    gyr_data_z = 0x08
    temp_data = 0x09
    sensor_time_0 = 0x0A
    sensor_time_1 = 0x0B
    sat_flags = 0x0C
    int_status_int1 = 0x0D
    int_status_int2 = 0x0E
    int_status_ibi = 0x0F
    feature_io0 = 0x10
    feature_io1 = 0x11
    feature_io2 = 0x12
    feature_io3 = 0x13
    feature_io_status = 0x14
    fifo_fill_level = 0x15
    fifo_data = 0x16
    acc_conf = 0x20
    gyr_conf = 0x21
    alt_acc_conf = 0x28
    alt_gyr_conf = 0x29
    alt_conf = 0x2A
    alt_status = 0x2B
    fifo_watermark = 0x35
    fifo_conf = 0x36
    fifo_ctrl = 0x37
    io_int_ctrl = 0x38
    int_conf = 0x39
    int_map1 = 0x3A
    int_map2 = 0x3B
    feature_ctrl = 0x40
    feature_data_addr = 0x41
    feature_data_tx = 0x42
    feature_data_status = 0x43
    feature_engine_status = 0x45
    feature_event_ext = 0x47
    io_pdn_ctrl = 0x4F
    io_spi_if = 0x50
    io_pad_strength = 0x51
    io_i2c_if = 0x52
    io_odr_derivation = 0x53
    acc_dp_off_x = 0x60
    acc_dp_dgain_x = 0x61
    acc_dp_off_y = 0x62
    acc_dp_dgain_y = 0x63
    acc_dp_off_z = 0x64
    acc_dp_dgain_z = 0x65
    gyr_dp_off_x = 0x66
    gyr_dp_dgain_x = 0x67
    gyr_dp_off_y = 0x68
    gyr_dp_dgain_y = 0x69
    gyr_dp_off_z = 0x6A
    gyr_dp_dgain_z = 0x6B
    i3c_tc_sync_tph = 0x70
    i3c_tc_sync_tu = 0x71
    i3c_tc_sync_odr = 0x72
    cmd = 0x7E
    cfg_res = 0x7F


class BMI323:
    def __init__(self) -> None:
        self.read: Callable | None = None
        self.write: Callable | None = None

    def assign_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read = read_callback
        self.write = write_callback

    @property
    def chip_id(self) -> int:
        return self.read(BMI323Addr.chip_id) & 0xFF

    @property
    def err_reg(self) -> int:
        return self.read(BMI323Addr.err_reg)

    @err_reg.setter
    def err_reg(self, value: int) -> None:
        self.write(BMI323Addr.err_reg, value)

    @property
    def status(self) -> int:
        return self.read(BMI323Addr.status)

    @status.setter
    def status(self, value: int) -> None:
        self.write(BMI323Addr.status, value)

    @property
    def acc_data(self) -> tuple[int, int, int]:
        payload = self.read(BMI323Addr.acc_data_x, 6)
        a_x, a_y, a_z = struct.unpack("<hhh", payload)
        return a_x, a_y, a_z

    @property
    def gyr_data(self) -> tuple[int, int, int]:
        payload = self.read(BMI323Addr.gyr_data_x, 6)
        g_x, g_y, g_z = struct.unpack("<hhh", payload)
        return g_x, g_y, g_z

    @property
    def temp_data(self) -> int:
        return self.read(BMI323Addr.temp_data)

    @property
    def sensor_time(self) -> int:
        sensor_time_0 = self.read(BMI323Addr.sensor_time_0)
        sensor_time_1 = self.read(BMI323Addr.sensor_time_1)
        return (sensor_time_1 << 16) | sensor_time_0

    @property
    def sat_flags(self) -> int:
        return self.read(BMI323Addr.sat_flags)

    @property
    def int_status_int1(self) -> int:
        return self.read(BMI323Addr.int_status_int1)

    @property
    def int_status_int2(self) -> int:
        return self.read(BMI323Addr.int_status_int2)

    @property
    def int_status_ibi(self) -> int:
        return self.read(BMI323Addr.int_status_ibi)

    @property
    def feature_io0(self) -> int:
        return self.read(BMI323Addr.feature_io0)

    @feature_io0.setter
    def feature_io0(self, value: int) -> None:
        self.write(BMI323Addr.feature_io0, value)

    @property
    def feature_io1(self) -> int:
        return self.read(BMI323Addr.feature_io1)

    @property
    def feature_io2(self) -> int:
        return self.read(BMI323Addr.feature_io2)

    @property
    def feature_io3(self) -> int:
        return self.read(BMI323Addr.feature_io3)

    @property
    def feature_io_status(self) -> int:
        return self.read(BMI323Addr.feature_io_status)

    @feature_io_status.setter
    def feature_io_status(self, value: int) -> None:
        self.write(BMI323Addr.feature_io_status, value)

    @property
    def fifo_fill_level(self) -> int:
        return self.read(BMI323Addr.fifo_fill_level)

    @property
    def fifo_data(self) -> int:
        return self.read(BMI323Addr.fifo_data)

    @fifo_data.setter
    def fifo_data(self, value: int) -> None:
        self.write(BMI323Addr.fifo_data, value)

    @property
    def acc_conf(self) -> int:
        return self.read(BMI323Addr.acc_conf)

    @acc_conf.setter
    def acc_conf(self, value: int) -> None:
        self.write(BMI323Addr.acc_conf, value)

    @property
    def gyr_conf(self) -> int:
        return self.read(BMI323Addr.gyr_conf)

    @gyr_conf.setter
    def gyr_conf(self, value: int) -> None:
        self.write(BMI323Addr.gyr_conf, value)

    @property
    def alt_acc_conf(self) -> int:
        return self.read(BMI323Addr.alt_acc_conf)

    @alt_acc_conf.setter
    def alt_acc_conf(self, value: int) -> None:
        self.write(BMI323Addr.alt_acc_conf, value)

    @property
    def alt_gyr_conf(self) -> int:
        return self.read(BMI323Addr.alt_gyr_conf)

    @alt_gyr_conf.setter
    def alt_gyr_conf(self, value: int) -> None:
        self.write(BMI323Addr.alt_gyr_conf, value)

    @property
    def alt_conf(self) -> int:
        return self.read(BMI323Addr.alt_conf)

    @alt_conf.setter
    def alt_conf(self, value: int) -> None:
        self.write(BMI323Addr.alt_conf, value)

    @property
    def alt_status(self) -> int:
        return self.read(BMI323Addr.alt_status)

    @property
    def fifo_watermark(self) -> int:
        return self.read(BMI323Addr.fifo_watermark)

    @fifo_watermark.setter
    def fifo_watermark(self, value: int) -> None:
        self.write(BMI323Addr.fifo_watermark, value)

    @property
    def fifo_conf(self) -> int:
        return self.read(BMI323Addr.fifo_conf)

    @fifo_conf.setter
    def fifo_conf(self, value: int) -> None:
        self.write(BMI323Addr.fifo_conf, value)

    def fifo_ctrl(self, value: int) -> None:
        self.write(BMI323Addr.fifo_ctrl, value)

    fifo_ctrl = property(None, fifo_ctrl)

    @property
    def io_int_ctrl(self) -> int:
        return self.read(BMI323Addr.io_int_ctrl)

    @io_int_ctrl.setter
    def io_int_ctrl(self, value: int) -> None:
        self.write(BMI323Addr.io_int_ctrl, value)

    @property
    def int_conf(self) -> int:
        return self.read(BMI323Addr.int_conf)

    @int_conf.setter
    def int_conf(self, value: int) -> None:
        self.write(BMI323Addr.int_conf, value)

    @property
    def int_map1(self) -> int:
        return self.read(BMI323Addr.int_map1)

    @int_map1.setter
    def int_map1(self, value: int) -> None:
        self.write(BMI323Addr.int_map1, value)

    @property
    def int_map2(self) -> int:
        return self.read(BMI323Addr.int_map2)

    @int_map2.setter
    def int_map2(self, value: int) -> None:
        self.write(BMI323Addr.int_map2, value)

    @property
    def feature_ctrl(self) -> int:
        return self.read(BMI323Addr.feature_ctrl)

    @feature_ctrl.setter
    def feature_ctrl(self, value: int) -> None:
        self.write(BMI323Addr.feature_ctrl, value)

    @property
    def feature_data_addr(self) -> int:
        return self.read(BMI323Addr.feature_data_addr)

    @feature_data_addr.setter
    def feature_data_addr(self, value: int) -> None:
        self.write(BMI323Addr.feature_data_addr, value)

    @property
    def feature_data_tx(self) -> int:
        return self.read(BMI323Addr.feature_data_tx)

    @feature_data_tx.setter
    def feature_data_tx(self, value: int) -> None:
        self.write(BMI323Addr.feature_data_tx, value)

    @property
    def feature_data_status(self) -> int:
        return self.read(BMI323Addr.feature_data_status)

    @property
    def feature_engine_status(self) -> int:
        return self.read(BMI323Addr.feature_engine_status)

    @property
    def feature_event_ext(self) -> int:
        return self.read(BMI323Addr.feature_event_ext)

    @property
    def io_pdn_ctrl(self) -> int:
        return self.read(BMI323Addr.io_pdn_ctrl)

    @io_pdn_ctrl.setter
    def io_pdn_ctrl(self, value: int) -> None:
        self.write(BMI323Addr.io_pdn_ctrl, value)

    @property
    def io_spi_if(self) -> int:
        return self.read(BMI323Addr.io_spi_if)

    @io_spi_if.setter
    def io_spi_if(self, value: int) -> None:
        self.write(BMI323Addr.io_spi_if, value)

    @property
    def io_pad_strength(self) -> int:
        return self.read(BMI323Addr.io_pad_strength)

    @io_pad_strength.setter
    def io_pad_strength(self, value: int) -> None:
        self.write(BMI323Addr.io_pad_strength, value)

    @property
    def io_i2c_if(self) -> int:
        return self.read(BMI323Addr.io_i2c_if)

    @io_i2c_if.setter
    def io_i2c_if(self, value: int) -> None:
        self.write(BMI323Addr.io_i2c_if, value)

    @property
    def io_odr_derivation(self) -> int:
        return self.read(BMI323Addr.io_odr_derivation)

    @property
    def acc_dp_off_x(self) -> int:
        return self.read(BMI323Addr.acc_dp_off_x)

    @acc_dp_off_x.setter
    def acc_dp_off_x(self, value: int) -> None:
        self.write(BMI323Addr.acc_dp_off_x, value)

    @property
    def acc_dp_dgain_x(self) -> int:
        return self.read(BMI323Addr.acc_dp_dgain_x)

    @acc_dp_dgain_x.setter
    def acc_dp_dgain_x(self, value: int) -> None:
        self.write(BMI323Addr.acc_dp_dgain_x, value)

    @property
    def acc_dp_off_y(self) -> int:
        return self.read(BMI323Addr.acc_dp_off_y)

    @acc_dp_off_y.setter
    def acc_dp_off_y(self, value: int) -> None:
        self.write(BMI323Addr.acc_dp_off_y, value)

    @property
    def acc_dp_dgain_y(self) -> int:
        return self.read(BMI323Addr.acc_dp_dgain_y)

    @acc_dp_dgain_y.setter
    def acc_dp_dgain_y(self, value: int) -> None:
        self.write(BMI323Addr.acc_dp_dgain_y, value)

    @property
    def acc_dp_off_z(self) -> int:
        return self.read(BMI323Addr.acc_dp_off_z)

    @acc_dp_off_z.setter
    def acc_dp_off_z(self, value: int) -> None:
        self.write(BMI323Addr.acc_dp_off_z, value)

    @property
    def acc_dp_dgain_z(self) -> int:
        return self.read(BMI323Addr.acc_dp_dgain_z)

    @acc_dp_dgain_z.setter
    def acc_dp_dgain_z(self, value: int) -> None:
        self.write(BMI323Addr.acc_dp_dgain_z, value)

    @property
    def gyr_dp_off_x(self) -> int:
        return self.read(BMI323Addr.gyr_dp_off_x)

    @gyr_dp_off_x.setter
    def gyr_dp_off_x(self, value: int) -> None:
        self.write(BMI323Addr.gyr_dp_off_x, value)

    @property
    def gyr_dp_dgain_x(self) -> int:
        return self.read(BMI323Addr.gyr_dp_dgain_x)

    @gyr_dp_dgain_x.setter
    def gyr_dp_dgain_x(self, value: int) -> None:
        self.write(BMI323Addr.gyr_dp_dgain_x, value)

    @property
    def gyr_dp_off_y(self) -> int:
        return self.read(BMI323Addr.gyr_dp_off_y)

    @gyr_dp_off_y.setter
    def gyr_dp_off_y(self, value: int) -> None:
        self.write(BMI323Addr.gyr_dp_off_y, value)

    @property
    def gyr_dp_dgain_y(self) -> int:
        return self.read(BMI323Addr.gyr_dp_dgain_y)

    @gyr_dp_dgain_y.setter
    def gyr_dp_dgain_y(self, value: int) -> None:
        self.write(BMI323Addr.gyr_dp_dgain_y, value)

    @property
    def gyr_dp_off_z(self) -> int:
        return self.read(BMI323Addr.gyr_dp_off_z)

    @gyr_dp_off_z.setter
    def gyr_dp_off_z(self, value: int) -> None:
        self.write(BMI323Addr.gyr_dp_off_z, value)

    @property
    def gyr_dp_dgain_z(self) -> int:
        return self.read(BMI323Addr.gyr_dp_dgain_z)

    @gyr_dp_dgain_z.setter
    def gyr_dp_dgain_z(self, value: int) -> None:
        self.write(BMI323Addr.gyr_dp_dgain_z, value)

    @property
    def i3c_tc_sync_tph(self) -> int:
        return self.read(BMI323Addr.i3c_tc_sync_tph)

    @i3c_tc_sync_tph.setter
    def i3c_tc_sync_tph(self, value: int) -> None:
        self.write(BMI323Addr.i3c_tc_sync_tph, value)

    @property
    def i3c_tc_sync_tu(self) -> int:
        return self.read(BMI323Addr.i3c_tc_sync_tu)

    @i3c_tc_sync_tu.setter
    def i3c_tc_sync_tu(self, value: int) -> None:
        self.write(BMI323Addr.i3c_tc_sync_tu, value)

    @property
    def i3c_tc_sync_odr(self) -> int:
        return self.read(BMI323Addr.i3c_tc_sync_odr)

    @i3c_tc_sync_odr.setter
    def i3c_tc_sync_odr(self, value: int) -> None:
        self.write(BMI323Addr.i3c_tc_sync_odr, value)

    def cmd(self, value: int) -> None:
        self.write(BMI323Addr.cmd, value)

    cmd = property(None, cmd)

    @property
    def cfg_res(self) -> int:
        return self.read(BMI323Addr.cfg_res)

    @cfg_res.setter
    def cfg_res(self, value: int) -> None:
        self.write(BMI323Addr.cfg_res, value)
