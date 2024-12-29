import struct
from collections.abc import Callable
from enum import Enum


class BMA456Addr(Enum):
    chip_id = 0x00
    err_reg = 0x02
    status = 0x03
    aux_x_lsb = 0x0A
    aux_x_msb = 0x0B
    aux_y_lsb = 0x0C
    aux_y_msb = 0x0D
    aux_z_lsb = 0x0E
    aux_z_msb = 0x0F
    aux_r_lsb = 0x10
    aux_r_msb = 0x11
    acc_x_lsb = 0x12
    acc_x_msb = 0x13
    acc_y_lsb = 0x14
    acc_y_msb = 0x15
    acc_z_lsb = 0x16
    acc_z_msb = 0x17
    sensor_time_0 = 0x18
    sensor_time_1 = 0x19
    sensor_time_2 = 0x1A
    event = 0x1B
    int_status_0 = 0x1C
    int_status_1 = 0x1D
    step_counter_0 = 0x1E
    step_counter_1 = 0x1F
    step_counter_2 = 0x20
    step_counter_3 = 0x21
    temperature = 0x22
    fifo_length_0 = 0x24
    fifo_length_1 = 0x25
    fifo_data = 0x26
    activity_type = 0x27
    internal_status = 0x2A
    acc_conf = 0x40
    acc_range = 0x41
    aux_conf = 0x44
    fifo_downs = 0x45
    fifo_wtm_0 = 0x46
    fifo_wtm_1 = 0x47
    fifo_config_0 = 0x48
    fifo_config_1 = 0x49
    aux_dev_id = 0x4B
    aux_if_conf = 0x4C
    aux_rd_addr = 0x4D
    aux_wr_addr = 0x4E
    aux_wr_data = 0x4F
    int1_io_ctrl = 0x53
    int2_io_ctrl = 0x54
    int_latch = 0x55
    int1_map = 0x56
    int2_map = 0x57
    int_map_data = 0x58
    init_ctrl = 0x59
    features_offset_lsb = 0x5B
    features_offset_msb = 0x5C
    features_in = 0x5E
    internal_error = 0x5F
    nvm_conf = 0x6A
    if_conf = 0x6B
    acc_self_test = 0x6D
    nv_conf = 0x70
    offset_0 = 0x71
    offset_1 = 0x72
    offset_2 = 0x73
    pwr_conf = 0x7C
    pwr_ctrl = 0x7D
    cmd = 0x7E


class BMA456:
    def __init__(self) -> None:
        self.read: Callable | None = None
        self.write: Callable | None = None

    def assign_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read = read_callback
        self.write = write_callback

    @property
    def chip_id(self) -> int:
        return self.read(BMA456Addr.chip_id)

    @property
    def err_reg(self) -> int:
        return self.read(BMA456Addr.err_reg)

    @property
    def status(self) -> int:
        return self.read(BMA456Addr.status)

    @property
    def aux_data(self) -> tuple[int, int, int, int]:
        payload = self.read(BMA456Addr.aux_x_lsb, 8)
        aux_x, aux_y, aux_z, aux_r = struct.unpack("<hhhh", payload)
        return aux_x, aux_y, aux_z, aux_r

    @property
    def acc_data(self) -> tuple[int, int, int]:
        payload = self.read(BMA456Addr.acc_x_lsb, 6)
        a_x, a_y, a_z = struct.unpack("<hhh", payload)
        return a_x, a_y, a_z

    @property
    def sensor_time(self) -> float:
        b_0, b_1, b_2 = self.read(BMA456Addr.sensor_time_0, 3)
        return ((b_2 << 16) | (b_1 << 8) | b_0) * 39.0625e-6

    @property
    def event(self) -> int:
        return self.read(BMA456Addr.event)

    @property
    def int_status_0(self) -> int:
        return self.read(BMA456Addr.int_status_0)

    @property
    def int_status_1(self) -> int:
        return self.read(BMA456Addr.int_status_1)

    @property
    def step_count(self) -> int:
        payload = self.read(BMA456Addr.step_counter_0, 4)
        (steps,) = struct.unpack("<I", payload)
        return steps

    @property
    def temperature(self) -> int:
        return self.read(BMA456Addr.temperature)

    @property
    def fifo_length_0(self) -> int:
        return self.read(BMA456Addr.fifo_length_0)

    @property
    def fifo_length_1(self) -> int:
        return self.read(BMA456Addr.fifo_length_1)

    @property
    def fifo_data(self) -> int:
        return self.read(BMA456Addr.fifo_data)

    @property
    def activity_type(self) -> int:
        return self.read(BMA456Addr.activity_type)

    @activity_type.setter
    def activity_type(self, value: int) -> None:
        self.write(BMA456Addr.activity_type, value)

    @property
    def internal_status(self) -> int:
        return self.read(BMA456Addr.internal_status)

    @property
    def acc_conf(self) -> int:
        return self.read(BMA456Addr.acc_conf)

    @acc_conf.setter
    def acc_conf(self, value: int) -> None:
        self.write(BMA456Addr.acc_conf, value)

    @property
    def acc_range(self) -> int:
        return self.read(BMA456Addr.acc_range)

    @acc_range.setter
    def acc_range(self, value: int) -> None:
        self.write(BMA456Addr.acc_range, value)

    @property
    def aux_conf(self) -> int:
        return self.read(BMA456Addr.aux_conf)

    @aux_conf.setter
    def aux_conf(self, value: int) -> None:
        self.write(BMA456Addr.aux_conf, value)

    @property
    def fifo_downs(self) -> int:
        return self.read(BMA456Addr.fifo_downs)

    @fifo_downs.setter
    def fifo_downs(self, value: int) -> None:
        self.write(BMA456Addr.fifo_downs, value)

    @property
    def fifo_wtm_0(self) -> int:
        return self.read(BMA456Addr.fifo_wtm_0)

    @fifo_wtm_0.setter
    def fifo_wtm_0(self, value: int) -> None:
        self.write(BMA456Addr.fifo_wtm_0, value)

    @property
    def fifo_wtm_1(self) -> int:
        return self.read(BMA456Addr.fifo_wtm_1)

    @fifo_wtm_1.setter
    def fifo_wtm_1(self, value: int) -> None:
        self.write(BMA456Addr.fifo_wtm_1, value)

    @property
    def fifo_config_0(self) -> int:
        return self.read(BMA456Addr.fifo_config_0)

    @fifo_config_0.setter
    def fifo_config_0(self, value: int) -> None:
        self.write(BMA456Addr.fifo_config_0, value)

    @property
    def fifo_config_1(self) -> int:
        return self.read(BMA456Addr.fifo_config_1)

    @fifo_config_1.setter
    def fifo_config_1(self, value: int) -> None:
        self.write(BMA456Addr.fifo_config_1, value)

    @property
    def aux_dev_id(self) -> int:
        return self.read(BMA456Addr.aux_dev_id)

    @aux_dev_id.setter
    def aux_dev_id(self, value: int) -> None:
        self.write(BMA456Addr.aux_dev_id, value)

    @property
    def aux_if_conf(self) -> int:
        return self.read(BMA456Addr.aux_if_conf)

    @aux_if_conf.setter
    def aux_if_conf(self, value: int) -> None:
        self.write(BMA456Addr.aux_if_conf, value)

    @property
    def aux_rd_addr(self) -> int:
        return self.read(BMA456Addr.aux_rd_addr)

    @aux_rd_addr.setter
    def aux_rd_addr(self, value: int) -> None:
        self.write(BMA456Addr.aux_rd_addr, value)

    @property
    def aux_wr_addr(self) -> int:
        return self.read(BMA456Addr.aux_wr_addr)

    @aux_wr_addr.setter
    def aux_wr_addr(self, value: int) -> None:
        self.write(BMA456Addr.aux_wr_addr, value)

    @property
    def aux_wr_data(self) -> int:
        return self.read(BMA456Addr.aux_wr_data)

    @aux_wr_data.setter
    def aux_wr_data(self, value: int) -> None:
        self.write(BMA456Addr.aux_wr_data, value)

    @property
    def int1_io_ctrl(self) -> int:
        return self.read(BMA456Addr.int1_io_ctrl)

    @int1_io_ctrl.setter
    def int1_io_ctrl(self, value: int) -> None:
        self.write(BMA456Addr.int1_io_ctrl, value)

    @property
    def int2_io_ctrl(self) -> int:
        return self.read(BMA456Addr.int2_io_ctrl)

    @int2_io_ctrl.setter
    def int2_io_ctrl(self, value: int) -> None:
        self.write(BMA456Addr.int2_io_ctrl, value)

    @property
    def int_latch(self) -> int:
        return self.read(BMA456Addr.int_latch)

    @int_latch.setter
    def int_latch(self, value: int) -> None:
        self.write(BMA456Addr.int_latch, value)

    @property
    def int1_map(self) -> int:
        return self.read(BMA456Addr.int1_map)

    @int1_map.setter
    def int1_map(self, value: int) -> None:
        self.write(BMA456Addr.int1_map, value)

    @property
    def int2_map(self) -> int:
        return self.read(BMA456Addr.int2_map)

    @int2_map.setter
    def int2_map(self, value: int) -> None:
        self.write(BMA456Addr.int2_map, value)

    @property
    def int_map_data(self) -> int:
        return self.read(BMA456Addr.int_map_data)

    @int_map_data.setter
    def int_map_data(self, value: int) -> None:
        self.write(BMA456Addr.int_map_data, value)

    @property
    def init_ctrl(self) -> int:
        return self.read(BMA456Addr.init_ctrl)

    @init_ctrl.setter
    def init_ctrl(self, value: int) -> None:
        self.write(BMA456Addr.init_ctrl, value)

    @property
    def features_offset_lsb(self) -> int:
        return self.read(BMA456Addr.features_offset_lsb)

    @features_offset_lsb.setter
    def features_offset_lsb(self, value: int) -> None:
        self.write(BMA456Addr.features_offset_lsb, value)

    @property
    def features_offset_msb(self) -> int:
        return self.read(BMA456Addr.features_offset_msb)

    @features_offset_msb.setter
    def features_offset_msb(self, value: int) -> None:
        self.write(BMA456Addr.features_offset_msb, value)

    @property
    def features_in(self) -> int:
        return self.read(BMA456Addr.features_in)

    @features_in.setter
    def features_in(self, value: int) -> None:
        self.write(BMA456Addr.features_in, value)

    @property
    def internal_error(self) -> int:
        return self.read(BMA456Addr.internal_error)

    @internal_error.setter
    def internal_error(self, value: int) -> None:
        self.write(BMA456Addr.internal_error, value)

    @property
    def nvm_conf(self) -> int:
        return self.read(BMA456Addr.nvm_conf)

    @nvm_conf.setter
    def nvm_conf(self, value: int) -> None:
        self.write(BMA456Addr.nvm_conf, value)

    @property
    def if_conf(self) -> int:
        return self.read(BMA456Addr.if_conf)

    @if_conf.setter
    def if_conf(self, value: int) -> None:
        self.write(BMA456Addr.if_conf, value)

    @property
    def acc_self_test(self) -> int:
        return self.read(BMA456Addr.acc_self_test)

    @acc_self_test.setter
    def acc_self_test(self, value: int) -> None:
        self.write(BMA456Addr.acc_self_test, value)

    @property
    def nv_conf(self) -> int:
        return self.read(BMA456Addr.nv_conf)

    @nv_conf.setter
    def nv_conf(self, value: int) -> None:
        self.write(BMA456Addr.nv_conf, value)

    @property
    def offset_0(self) -> int:
        return self.read(BMA456Addr.offset_0)

    @offset_0.setter
    def offset_0(self, value: int) -> None:
        self.write(BMA456Addr.offset_0, value)

    @property
    def offset_1(self) -> int:
        return self.read(BMA456Addr.offset_1)

    @offset_1.setter
    def offset_1(self, value: int) -> None:
        self.write(BMA456Addr.offset_1, value)

    @property
    def offset_2(self) -> int:
        return self.read(BMA456Addr.offset_2)

    @offset_2.setter
    def offset_2(self, value: int) -> None:
        self.write(BMA456Addr.offset_2, value)

    @property
    def pwr_conf(self) -> int:
        return self.read(BMA456Addr.pwr_conf)

    @pwr_conf.setter
    def pwr_conf(self, value: int) -> None:
        self.write(BMA456Addr.pwr_conf, value)

    @property
    def pwr_ctrl(self) -> int:
        return self.read(BMA456Addr.pwr_ctrl)

    @pwr_ctrl.setter
    def pwr_ctrl(self, value: int) -> None:
        self.write(BMA456Addr.pwr_ctrl, value)

    @property
    def cmd(self) -> int:
        return self.read(BMA456Addr.cmd)

    @cmd.setter
    def cmd(self, value: int) -> None:
        self.write(BMA456Addr.cmd, value)
