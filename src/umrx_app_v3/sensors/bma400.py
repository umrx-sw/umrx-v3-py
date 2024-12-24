import struct
from collections.abc import Callable
from enum import Enum


class BMA400Addr(Enum):
    chip_id = 0x00
    err_reg = 0x02
    status = 0x03
    acc_x_lsb = 0x04
    acc_x_msb = 0x05
    acc_y_lsb = 0x06
    acc_y_msb = 0x07
    acc_z_lsb = 0x08
    acc_z_msb = 0x09
    sensor_time_0 = 0x0A
    sensor_time_1 = 0x0B
    sensor_time_2 = 0x0C
    event = 0x0D
    int_stat_0 = 0x0E
    int_stat_1 = 0x0F
    int_stat_2 = 0x10
    temp_data = 0x11
    fifo_length_0 = 0x12
    fifo_length_1 = 0x13
    fifo_data = 0x14
    step_cnt_0 = 0x15
    step_cnt_1 = 0x16
    step_cnt_2 = 0x17
    step_stat = 0x18
    acc_config_0 = 0x19
    acc_config_1 = 0x1A
    acc_config_2 = 0x1B
    int_config_0 = 0x1F
    int_config_1 = 0x20
    int1_map = 0x21
    int2_map = 0x22
    int12_map = 0x23
    int12_io_ctlr = 0x24
    fifo_config_0 = 0x26
    fifo_config_1 = 0x27
    fifo_config_2 = 0x28
    fifo_pwr_config = 0x29
    auto_low_pow_0 = 0x2A
    auto_low_pow_1 = 0x2B
    auto_wake_up_0 = 0x2C
    auto_wake_up_1 = 0x2D
    wkup_int_config_0 = 0x2F
    wkup_int_config_1 = 0x30
    wkup_int_config_2 = 0x31
    wkup_int_config_3 = 0x32
    wkup_int_config_4 = 0x33
    orient_ch_config_0 = 0x35
    orient_ch_config_1 = 0x36
    orient_ch_config_3 = 0x38
    orient_ch_config_4 = 0x39
    orient_ch_config_5 = 0x3A
    orient_ch_config_6 = 0x3B
    orient_ch_config_7 = 0x3C
    orient_ch_config_8 = 0x3D
    orient_ch_config_9 = 0x3E
    gen1_int_config_0 = 0x3F
    gen1_int_config_1 = 0x40
    gen1_int_config_2 = 0x41
    gen1_int_config_3 = 0x42
    gen1_int_config_31 = 0x43
    gen1_int_config_4 = 0x44
    gen1_int_config_5 = 0x45
    gen1_int_config_6 = 0x46
    gen1_int_config_7 = 0x47
    gen1_int_config_8 = 0x48
    gen1_int_config_9 = 0x49
    gen2_int_config_0 = 0x4A
    gen2_int_config_1 = 0x4B
    gen2_int_config_2 = 0x4C
    gen2_int_config_3 = 0x4D
    gen2_int_config_31 = 0x4E
    gen2_int_config_4 = 0x4F
    gen2_int_config_5 = 0x50
    gen2_int_config_6 = 0x51
    gen2_int_config_7 = 0x52
    gen2_int_config_8 = 0x53
    gen2_int_config_9 = 0x54
    acth_config_0 = 0x55
    acth_config_1 = 0x56
    tap_config = 0x57
    tap_config_1 = 0x58
    if_conf = 0x7C
    self_test = 0x7D
    cmd = 0x7E


class BMA400:
    def __init__(self) -> None:
        self.read: Callable | None = None
        self.write: Callable | None = None

    def assign_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read = read_callback
        self.write = write_callback

    @staticmethod
    def sign_convert_accel(a_x: int, a_y: int, a_z: int) -> tuple[int, int, int]:
        if a_x > 2047:
            a_x -= 4096
        if a_y > 2047:
            a_y -= 4096
        if a_z > 2047:
            a_z -= 4096
        return a_x, a_y, a_z

    @property
    def chip_id(self) -> int:
        return self.read(BMA400Addr.chip_id)

    @property
    def err_reg(self) -> int:
        return self.read(BMA400Addr.err_reg)

    @property
    def status(self) -> int:
        return self.read(BMA400Addr.status)

    @property
    def acc_data(self) -> tuple[int, int, int]:
        payload = self.read(BMA400Addr.acc_x_lsb, 6)
        a_x, a_y, a_z = struct.unpack("<HHH", payload)
        a_x, a_y, a_z = BMA400.sign_convert_accel(a_x, a_y, a_z)
        return a_x, a_y, a_z

    @property
    def sensor_time(self) -> float:
        b_0, b_1, b_2 = self.read(BMA400Addr.sensor_time_0, 3)
        return ((b_2 << 16) | (b_1 << 8) | b_0) * 39.0625e-6

    @property
    def event(self) -> int:
        return self.read(BMA400Addr.event)

    @property
    def int_stat_0(self) -> int:
        return self.read(BMA400Addr.int_stat_0)

    @property
    def int_stat_1(self) -> int:
        return self.read(BMA400Addr.int_stat_1)

    @property
    def int_stat_2(self) -> int:
        return self.read(BMA400Addr.int_stat_2)

    @property
    def temp_data(self) -> int:
        return self.read(BMA400Addr.temp_data)

    @property
    def fifo_length_0(self) -> int:
        return self.read(BMA400Addr.fifo_length_0)

    @property
    def fifo_length_1(self) -> int:
        return self.read(BMA400Addr.fifo_length_1)

    @property
    def fifo_data(self) -> int:
        return self.read(BMA400Addr.fifo_data)

    @property
    def step_count(self) -> int:
        b_0, b_1, b_2 = self.read(BMA400Addr.step_cnt_0, 3)
        return (b_2 << 16) | (b_1 << 8) | b_0

    @property
    def step_stat(self) -> int:
        return self.read(BMA400Addr.step_stat)

    @property
    def acc_config_0(self) -> int:
        return self.read(BMA400Addr.acc_config_0)

    @acc_config_0.setter
    def acc_config_0(self, value: int) -> None:
        self.write(BMA400Addr.acc_config_0, value)

    @property
    def acc_config_1(self) -> int:
        return self.read(BMA400Addr.acc_config_1)

    @acc_config_1.setter
    def acc_config_1(self, value: int) -> None:
        self.write(BMA400Addr.acc_config_1, value)

    @property
    def acc_config_2(self) -> int:
        return self.read(BMA400Addr.acc_config_2)

    @acc_config_2.setter
    def acc_config_2(self, value: int) -> None:
        self.write(BMA400Addr.acc_config_2, value)

    @property
    def int_config_0(self) -> int:
        return self.read(BMA400Addr.int_config_0)

    @int_config_0.setter
    def int_config_0(self, value: int) -> None:
        self.write(BMA400Addr.int_config_0, value)

    @property
    def int_config_1(self) -> int:
        return self.read(BMA400Addr.int_config_1)

    @int_config_1.setter
    def int_config_1(self, value: int) -> None:
        self.write(BMA400Addr.int_config_1, value)

    @property
    def int1_map(self) -> int:
        return self.read(BMA400Addr.int1_map)

    @int1_map.setter
    def int1_map(self, value: int) -> None:
        self.write(BMA400Addr.int1_map, value)

    @property
    def int2_map(self) -> int:
        return self.read(BMA400Addr.int2_map)

    @int2_map.setter
    def int2_map(self, value: int) -> None:
        self.write(BMA400Addr.int2_map, value)

    @property
    def int12_map(self) -> int:
        return self.read(BMA400Addr.int12_map)

    @int12_map.setter
    def int12_map(self, value: int) -> None:
        self.write(BMA400Addr.int12_map, value)

    @property
    def int12_io_ctlr(self) -> int:
        return self.read(BMA400Addr.int12_io_ctlr)

    @int12_io_ctlr.setter
    def int12_io_ctlr(self, value: int) -> None:
        self.write(BMA400Addr.int12_io_ctlr, value)

    @property
    def fifo_config_0(self) -> int:
        return self.read(BMA400Addr.fifo_config_0)

    @fifo_config_0.setter
    def fifo_config_0(self, value: int) -> None:
        self.write(BMA400Addr.fifo_config_0, value)

    @property
    def fifo_config_1(self) -> int:
        return self.read(BMA400Addr.fifo_config_1)

    @fifo_config_1.setter
    def fifo_config_1(self, value: int) -> None:
        self.write(BMA400Addr.fifo_config_1, value)

    @property
    def fifo_config_2(self) -> int:
        return self.read(BMA400Addr.fifo_config_2)

    @fifo_config_2.setter
    def fifo_config_2(self, value: int) -> None:
        self.write(BMA400Addr.fifo_config_2, value)

    @property
    def fifo_pwr_config(self) -> int:
        return self.read(BMA400Addr.fifo_pwr_config)

    @fifo_pwr_config.setter
    def fifo_pwr_config(self, value: int) -> None:
        self.write(BMA400Addr.fifo_pwr_config, value)

    @property
    def auto_low_pow_0(self) -> int:
        return self.read(BMA400Addr.auto_low_pow_0)

    @auto_low_pow_0.setter
    def auto_low_pow_0(self, value: int) -> None:
        self.write(BMA400Addr.auto_low_pow_0, value)

    @property
    def auto_low_pow_1(self) -> int:
        return self.read(BMA400Addr.auto_low_pow_1)

    @auto_low_pow_1.setter
    def auto_low_pow_1(self, value: int) -> None:
        self.write(BMA400Addr.auto_low_pow_1, value)

    @property
    def auto_wake_up_0(self) -> int:
        return self.read(BMA400Addr.auto_wake_up_0)

    @auto_wake_up_0.setter
    def auto_wake_up_0(self, value: int) -> None:
        self.write(BMA400Addr.auto_wake_up_0, value)

    @property
    def auto_wake_up_1(self) -> int:
        return self.read(BMA400Addr.auto_wake_up_1)

    @auto_wake_up_1.setter
    def auto_wake_up_1(self, value: int) -> None:
        self.write(BMA400Addr.auto_wake_up_1, value)

    @property
    def wkup_int_config_0(self) -> int:
        return self.read(BMA400Addr.wkup_int_config_0)

    @wkup_int_config_0.setter
    def wkup_int_config_0(self, value: int) -> None:
        self.write(BMA400Addr.wkup_int_config_0, value)

    @property
    def wkup_int_config_1(self) -> int:
        return self.read(BMA400Addr.wkup_int_config_1)

    @wkup_int_config_1.setter
    def wkup_int_config_1(self, value: int) -> None:
        self.write(BMA400Addr.wkup_int_config_1, value)

    @property
    def wkup_int_config_2(self) -> int:
        return self.read(BMA400Addr.wkup_int_config_2)

    @wkup_int_config_2.setter
    def wkup_int_config_2(self, value: int) -> None:
        self.write(BMA400Addr.wkup_int_config_2, value)

    @property
    def wkup_int_config_3(self) -> int:
        return self.read(BMA400Addr.wkup_int_config_3)

    @wkup_int_config_3.setter
    def wkup_int_config_3(self, value: int) -> None:
        self.write(BMA400Addr.wkup_int_config_3, value)

    @property
    def wkup_int_config_4(self) -> int:
        return self.read(BMA400Addr.wkup_int_config_4)

    @wkup_int_config_4.setter
    def wkup_int_config_4(self, value: int) -> None:
        self.write(BMA400Addr.wkup_int_config_4, value)

    @property
    def orient_ch_config_0(self) -> int:
        return self.read(BMA400Addr.orient_ch_config_0)

    @orient_ch_config_0.setter
    def orient_ch_config_0(self, value: int) -> None:
        self.write(BMA400Addr.orient_ch_config_0, value)

    @property
    def orient_ch_config_1(self) -> int:
        return self.read(BMA400Addr.orient_ch_config_1)

    @orient_ch_config_1.setter
    def orient_ch_config_1(self, value: int) -> None:
        self.write(BMA400Addr.orient_ch_config_1, value)

    @property
    def orient_ch_config_3(self) -> int:
        return self.read(BMA400Addr.orient_ch_config_3)

    @orient_ch_config_3.setter
    def orient_ch_config_3(self, value: int) -> None:
        self.write(BMA400Addr.orient_ch_config_3, value)

    @property
    def orient_ch_config_4(self) -> int:
        return self.read(BMA400Addr.orient_ch_config_4)

    @orient_ch_config_4.setter
    def orient_ch_config_4(self, value: int) -> None:
        self.write(BMA400Addr.orient_ch_config_4, value)

    @property
    def orient_ch_config_5(self) -> int:
        return self.read(BMA400Addr.orient_ch_config_5)

    @orient_ch_config_5.setter
    def orient_ch_config_5(self, value: int) -> None:
        self.write(BMA400Addr.orient_ch_config_5, value)

    @property
    def orient_ch_config_6(self) -> int:
        return self.read(BMA400Addr.orient_ch_config_6)

    @orient_ch_config_6.setter
    def orient_ch_config_6(self, value: int) -> None:
        self.write(BMA400Addr.orient_ch_config_6, value)

    @property
    def orient_ch_config_7(self) -> int:
        return self.read(BMA400Addr.orient_ch_config_7)

    @orient_ch_config_7.setter
    def orient_ch_config_7(self, value: int) -> None:
        self.write(BMA400Addr.orient_ch_config_7, value)

    @property
    def orient_ch_config_8(self) -> int:
        return self.read(BMA400Addr.orient_ch_config_8)

    @orient_ch_config_8.setter
    def orient_ch_config_8(self, value: int) -> None:
        self.write(BMA400Addr.orient_ch_config_8, value)

    @property
    def orient_ch_config_9(self) -> int:
        return self.read(BMA400Addr.orient_ch_config_9)

    @orient_ch_config_9.setter
    def orient_ch_config_9(self, value: int) -> None:
        self.write(BMA400Addr.orient_ch_config_9, value)

    @property
    def gen1_int_config_0(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_0)

    @gen1_int_config_0.setter
    def gen1_int_config_0(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_0, value)

    @property
    def gen1_int_config_1(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_1)

    @gen1_int_config_1.setter
    def gen1_int_config_1(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_1, value)

    @property
    def gen1_int_config_2(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_2)

    @gen1_int_config_2.setter
    def gen1_int_config_2(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_2, value)

    @property
    def gen1_int_config_3(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_3)

    @gen1_int_config_3.setter
    def gen1_int_config_3(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_3, value)

    @property
    def gen1_int_config_31(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_31)

    @gen1_int_config_31.setter
    def gen1_int_config_31(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_31, value)

    @property
    def gen1_int_config_4(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_4)

    @gen1_int_config_4.setter
    def gen1_int_config_4(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_4, value)

    @property
    def gen1_int_config_5(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_5)

    @gen1_int_config_5.setter
    def gen1_int_config_5(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_5, value)

    @property
    def gen1_int_config_6(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_6)

    @gen1_int_config_6.setter
    def gen1_int_config_6(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_6, value)

    @property
    def gen1_int_config_7(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_7)

    @gen1_int_config_7.setter
    def gen1_int_config_7(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_7, value)

    @property
    def gen1_int_config_8(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_8)

    @gen1_int_config_8.setter
    def gen1_int_config_8(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_8, value)

    @property
    def gen1_int_config_9(self) -> int:
        return self.read(BMA400Addr.gen1_int_config_9)

    @gen1_int_config_9.setter
    def gen1_int_config_9(self, value: int) -> None:
        self.write(BMA400Addr.gen1_int_config_9, value)

    @property
    def gen2_int_config_0(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_0)

    @gen2_int_config_0.setter
    def gen2_int_config_0(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_0, value)

    @property
    def gen2_int_config_1(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_1)

    @gen2_int_config_1.setter
    def gen2_int_config_1(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_1, value)

    @property
    def gen2_int_config_2(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_2)

    @gen2_int_config_2.setter
    def gen2_int_config_2(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_2, value)

    @property
    def gen2_int_config_3(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_3)

    @gen2_int_config_3.setter
    def gen2_int_config_3(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_3, value)

    @property
    def gen2_int_config_31(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_31)

    @gen2_int_config_31.setter
    def gen2_int_config_31(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_31, value)

    @property
    def gen2_int_config_4(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_4)

    @gen2_int_config_4.setter
    def gen2_int_config_4(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_4, value)

    @property
    def gen2_int_config_5(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_5)

    @gen2_int_config_5.setter
    def gen2_int_config_5(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_5, value)

    @property
    def gen2_int_config_6(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_6)

    @gen2_int_config_6.setter
    def gen2_int_config_6(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_6, value)

    @property
    def gen2_int_config_7(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_7)

    @gen2_int_config_7.setter
    def gen2_int_config_7(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_7, value)

    @property
    def gen2_int_config_8(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_8)

    @gen2_int_config_8.setter
    def gen2_int_config_8(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_8, value)

    @property
    def gen2_int_config_9(self) -> int:
        return self.read(BMA400Addr.gen2_int_config_9)

    @gen2_int_config_9.setter
    def gen2_int_config_9(self, value: int) -> None:
        self.write(BMA400Addr.gen2_int_config_9, value)

    @property
    def acth_config_0(self) -> int:
        return self.read(BMA400Addr.acth_config_0)

    @acth_config_0.setter
    def acth_config_0(self, value: int) -> None:
        self.write(BMA400Addr.acth_config_0, value)

    @property
    def acth_config_1(self) -> int:
        return self.read(BMA400Addr.acth_config_1)

    @acth_config_1.setter
    def acth_config_1(self, value: int) -> None:
        self.write(BMA400Addr.acth_config_1, value)

    @property
    def tap_config(self) -> int:
        return self.read(BMA400Addr.tap_config)

    @tap_config.setter
    def tap_config(self, value: int) -> None:
        self.write(BMA400Addr.tap_config, value)

    @property
    def tap_config_1(self) -> int:
        return self.read(BMA400Addr.tap_config_1)

    @tap_config_1.setter
    def tap_config_1(self, value: int) -> None:
        self.write(BMA400Addr.tap_config_1, value)

    @property
    def if_conf(self) -> int:
        return self.read(BMA400Addr.if_conf)

    @if_conf.setter
    def if_conf(self, value: int) -> None:
        self.write(BMA400Addr.if_conf, value)

    @property
    def self_test(self) -> int:
        return self.read(BMA400Addr.self_test)

    @self_test.setter
    def self_test(self, value: int) -> None:
        self.write(BMA400Addr.self_test, value)

    @property
    def cmd(self) -> int:
        return self.read(BMA400Addr.cmd)

    @cmd.setter
    def cmd(self, value: int) -> None:
        self.write(BMA400Addr.cmd, value)
