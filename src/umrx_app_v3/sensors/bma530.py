import struct
from array import array
from collections.abc import Callable
from enum import Enum


class BMA530Addr(Enum):
    chip_id = 0x00
    health_status = 0x02
    cmd_suspend = 0x04
    config_status = 0x10
    sensor_status = 0x11
    int_status_int1_0 = 0x12
    int_status_int1_1 = 0x13
    int_status_int2_0 = 0x14
    int_status_int2_1 = 0x15
    int_status_i3c_0 = 0x16
    int_status_i3c_1 = 0x17
    acc_data_0 = 0x18
    acc_data_1 = 0x19
    acc_data_2 = 0x1A
    acc_data_3 = 0x1B
    acc_data_4 = 0x1C
    acc_data_5 = 0x1D
    temp_data = 0x1E
    sensor_time_0 = 0x1F
    sensor_time_1 = 0x20
    sensor_time_2 = 0x21
    fifo_level_0 = 0x22
    fifo_level_1 = 0x23
    fifo_data_out = 0x24
    acc_conf_0 = 0x30
    acc_conf_1 = 0x31
    acc_conf_2 = 0x32
    temp_conf = 0x33
    int1_conf = 0x34
    int2_conf = 0x35
    int_map_0 = 0x36
    int_map_1 = 0x37
    int_map_2 = 0x38
    int_map_3 = 0x39
    if_conf_0 = 0x3A
    if_conf_1 = 0x3B
    fifo_ctrl = 0x40
    fifo_conf_0 = 0x41
    fifo_conf_1 = 0x42
    fifo_wm_0 = 0x43
    fifo_wm_1 = 0x44
    feat_eng_conf = 0x50
    feat_eng_status = 0x51
    feat_eng_gp_flags = 0x52
    feat_eng_gpr_conf = 0x53
    feat_eng_gpr_ctrl = 0x54
    feat_eng_gpr_0 = 0x55
    feat_eng_gpr_1 = 0x56
    feat_eng_gpr_2 = 0x57
    feat_eng_gpr_3 = 0x58
    feat_eng_gpr_4 = 0x59
    feat_eng_gpr_5 = 0x5A
    feature_data_addr = 0x5E
    feature_data_tx = 0x5F
    acc_offset_0 = 0x70
    acc_offset_1 = 0x71
    acc_offset_2 = 0x72
    acc_offset_3 = 0x73
    acc_offset_4 = 0x74
    acc_offset_5 = 0x75
    acc_self_test = 0x76
    cmd = 0x7E


class BMA530ExtendedAddr(Enum):
    feat_conf_err = 0x02
    general_settings_0 = 0x03
    generic_interrupt1_1 = 0x04
    generic_interrupt1_2 = 0x05
    generic_interrupt1_3 = 0x06
    generic_interrupt1_4 = 0x07
    generic_interrupt1_5 = 0x08
    generic_interrupt1_6 = 0x09
    generic_interrupt1_7 = 0x0A
    generic_interrupt2_1 = 0x0B
    generic_interrupt2_2 = 0x0C
    generic_interrupt2_3 = 0x0D
    generic_interrupt2_4 = 0x0E
    generic_interrupt2_5 = 0x0F
    generic_interrupt2_6 = 0x10
    generic_interrupt2_7 = 0x11
    generic_interrupt3_1 = 0x12
    generic_interrupt3_2 = 0x13
    generic_interrupt3_3 = 0x14
    generic_interrupt3_4 = 0x15
    generic_interrupt3_5 = 0x16
    generic_interrupt3_6 = 0x17
    generic_interrupt3_7 = 0x18
    step_counter = 0x19
    sig_motion = 0x2B
    tilt_1 = 0x2E
    tilt_2 = 0x2F
    orientation_1 = 0x30
    orientation_2 = 0x31
    foc_0 = 0x32
    foc_1 = 0x33
    foc_2 = 0x34
    foc_3 = 0x35


class BMA530:
    def __init__(self) -> None:
        self.read: Callable | None = None
        self.write: Callable | None = None

    def assign_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read = read_callback
        self.write = write_callback

    @property
    def chip_id(self) -> int:
        return self.read(BMA530Addr.chip_id)

    @property
    def health_status(self) -> int:
        return self.read(BMA530Addr.health_status)

    @property
    def cmd_suspend(self) -> int:
        return self.read(BMA530Addr.cmd_suspend)

    @cmd_suspend.setter
    def cmd_suspend(self, value: int) -> None:
        self.write(BMA530Addr.cmd_suspend, value)

    @property
    def config_status(self) -> int:
        return self.read(BMA530Addr.config_status)

    @config_status.setter
    def config_status(self, value: int) -> None:
        self.write(BMA530Addr.config_status, value)

    @property
    def sensor_status(self) -> int:
        return self.read(BMA530Addr.sensor_status)

    @sensor_status.setter
    def sensor_status(self, value: int) -> None:
        self.write(BMA530Addr.sensor_status, value)

    @property
    def int_status_int1_0(self) -> int:
        return self.read(BMA530Addr.int_status_int1_0)

    @int_status_int1_0.setter
    def int_status_int1_0(self, value: int) -> None:
        self.write(BMA530Addr.int_status_int1_0, value)

    @property
    def int_status_int1_1(self) -> int:
        return self.read(BMA530Addr.int_status_int1_1)

    @int_status_int1_1.setter
    def int_status_int1_1(self, value: int) -> None:
        self.write(BMA530Addr.int_status_int1_1, value)

    @property
    def int_status_int2_0(self) -> int:
        return self.read(BMA530Addr.int_status_int2_0)

    @int_status_int2_0.setter
    def int_status_int2_0(self, value: int) -> None:
        self.write(BMA530Addr.int_status_int2_0, value)

    @property
    def int_status_int2_1(self) -> int:
        return self.read(BMA530Addr.int_status_int2_1)

    @int_status_int2_1.setter
    def int_status_int2_1(self, value: int) -> None:
        self.write(BMA530Addr.int_status_int2_1, value)

    @property
    def int_status_i3c_0(self) -> int:
        return self.read(BMA530Addr.int_status_i3c_0)

    @int_status_i3c_0.setter
    def int_status_i3c_0(self, value: int) -> None:
        self.write(BMA530Addr.int_status_i3c_0, value)

    @property
    def int_status_i3c_1(self) -> int:
        return self.read(BMA530Addr.int_status_i3c_1)

    @int_status_i3c_1.setter
    def int_status_i3c_1(self, value: int) -> None:
        self.write(BMA530Addr.int_status_i3c_1, value)

    @property
    def acc_data(self) -> tuple[int, int, int]:
        payload = self.read(BMA530Addr.acc_data_0, 6)
        a_x, a_y, a_z = struct.unpack("<hhh", payload)
        return a_x, a_y, a_z

    @property
    def temperature(self) -> int:
        return self.read(BMA530Addr.temp_data)

    @property
    def sensor_time(self) -> int:
        byte_0, byte_1, byte_2 = self.read(BMA530Addr.sensor_time_0, 3)
        return (byte_2 << 16) | (byte_1 << 8) | byte_0

    @property
    def fifo_level(self) -> int:
        byte_0, byte_1 = self.read(BMA530Addr.fifo_level_0, 2)
        return ((0x07 & byte_1) << 8) | byte_0

    @property
    def fifo_data_out(self) -> int:
        return self.read(BMA530Addr.fifo_data_out)

    @property
    def acc_conf_0(self) -> int:
        return self.read(BMA530Addr.acc_conf_0)

    @acc_conf_0.setter
    def acc_conf_0(self, value: int) -> None:
        self.write(BMA530Addr.acc_conf_0, value)

    @property
    def acc_conf_1(self) -> int:
        return self.read(BMA530Addr.acc_conf_1)

    @acc_conf_1.setter
    def acc_conf_1(self, value: int) -> None:
        self.write(BMA530Addr.acc_conf_1, value)

    @property
    def acc_conf_2(self) -> int:
        return self.read(BMA530Addr.acc_conf_2)

    @acc_conf_2.setter
    def acc_conf_2(self, value: int) -> None:
        self.write(BMA530Addr.acc_conf_2, value)

    @property
    def temp_conf(self) -> int:
        return self.read(BMA530Addr.temp_conf)

    @temp_conf.setter
    def temp_conf(self, value: int) -> None:
        self.write(BMA530Addr.temp_conf, value)

    @property
    def int1_conf(self) -> int:
        return self.read(BMA530Addr.int1_conf)

    @int1_conf.setter
    def int1_conf(self, value: int) -> None:
        self.write(BMA530Addr.int1_conf, value)

    @property
    def int2_conf(self) -> int:
        return self.read(BMA530Addr.int2_conf)

    @int2_conf.setter
    def int2_conf(self, value: int) -> None:
        self.write(BMA530Addr.int2_conf, value)

    @property
    def int_map_0(self) -> int:
        return self.read(BMA530Addr.int_map_0)

    @int_map_0.setter
    def int_map_0(self, value: int) -> None:
        self.write(BMA530Addr.int_map_0, value)

    @property
    def int_map_1(self) -> int:
        return self.read(BMA530Addr.int_map_1)

    @int_map_1.setter
    def int_map_1(self, value: int) -> None:
        self.write(BMA530Addr.int_map_1, value)

    @property
    def int_map_2(self) -> int:
        return self.read(BMA530Addr.int_map_2)

    @int_map_2.setter
    def int_map_2(self, value: int) -> None:
        self.write(BMA530Addr.int_map_2, value)

    @property
    def int_map_3(self) -> int:
        return self.read(BMA530Addr.int_map_3)

    @int_map_3.setter
    def int_map_3(self, value: int) -> None:
        self.write(BMA530Addr.int_map_3, value)

    @property
    def if_conf_0(self) -> int:
        return self.read(BMA530Addr.if_conf_0)

    @property
    def if_conf_1(self) -> int:
        return self.read(BMA530Addr.if_conf_1)

    @if_conf_1.setter
    def if_conf_1(self, value: int) -> None:
        self.write(BMA530Addr.if_conf_1, value)

    def fifo_ctrl(self, value: int) -> None:
        self.write(BMA530Addr.fifo_ctrl, value)

    fifo_ctrl = property(None, fifo_ctrl)

    @property
    def fifo_conf_0(self) -> int:
        return self.read(BMA530Addr.fifo_conf_0)

    @fifo_conf_0.setter
    def fifo_conf_0(self, value: int) -> None:
        self.write(BMA530Addr.fifo_conf_0, value)

    @property
    def fifo_conf_1(self) -> int:
        return self.read(BMA530Addr.fifo_conf_1)

    @fifo_conf_1.setter
    def fifo_conf_1(self, value: int) -> None:
        self.write(BMA530Addr.fifo_conf_1, value)

    @property
    def fifo_wm_0(self) -> int:
        return self.read(BMA530Addr.fifo_wm_0)

    @fifo_wm_0.setter
    def fifo_wm_0(self, value: int) -> None:
        self.write(BMA530Addr.fifo_wm_0, value)

    @property
    def fifo_wm_1(self) -> int:
        return self.read(BMA530Addr.fifo_wm_1)

    @fifo_wm_1.setter
    def fifo_wm_1(self, value: int) -> None:
        self.write(BMA530Addr.fifo_wm_1, value)

    @property
    def feat_eng_conf(self) -> int:
        return self.read(BMA530Addr.feat_eng_conf)

    @feat_eng_conf.setter
    def feat_eng_conf(self, value: int) -> None:
        self.write(BMA530Addr.feat_eng_conf, value)

    @property
    def feat_eng_status(self) -> int:
        return self.read(BMA530Addr.feat_eng_status)

    @property
    def feat_eng_gp_flags(self) -> int:
        return self.read(BMA530Addr.feat_eng_gp_flags)

    @property
    def feat_eng_gpr_conf(self) -> int:
        return self.read(BMA530Addr.feat_eng_gpr_conf)

    @feat_eng_gpr_conf.setter
    def feat_eng_gpr_conf(self, value: int) -> None:
        self.write(BMA530Addr.feat_eng_gpr_conf, value)

    def feat_eng_gpr_ctrl(self, value: int) -> None:
        self.write(BMA530Addr.feat_eng_gpr_ctrl, value)

    feat_eng_gpr_ctrl = property(None, feat_eng_gpr_ctrl)

    @property
    def feat_eng_gpr_0(self) -> int:
        return self.read(BMA530Addr.feat_eng_gpr_0)

    @feat_eng_gpr_0.setter
    def feat_eng_gpr_0(self, value: int) -> None:
        self.write(BMA530Addr.feat_eng_gpr_0, value)

    @property
    def feat_eng_gpr_1(self) -> int:
        return self.read(BMA530Addr.feat_eng_gpr_1)

    @feat_eng_gpr_1.setter
    def feat_eng_gpr_1(self, value: int) -> None:
        self.write(BMA530Addr.feat_eng_gpr_1, value)

    @property
    def feat_eng_gpr_2(self) -> int:
        return self.read(BMA530Addr.feat_eng_gpr_2)

    @property
    def feat_eng_gpr_3(self) -> int:
        return self.read(BMA530Addr.feat_eng_gpr_3)

    @property
    def feat_eng_gpr_4(self) -> int:
        return self.read(BMA530Addr.feat_eng_gpr_4)

    @property
    def feat_eng_gpr_5(self) -> int:
        return self.read(BMA530Addr.feat_eng_gpr_5)

    @property
    def feature_data_addr(self) -> int:
        return self.read(BMA530Addr.feature_data_addr)

    @feature_data_addr.setter
    def feature_data_addr(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, value)

    @property
    def feature_data_tx(self) -> int:
        return self.read(BMA530Addr.feature_data_tx)

    @feature_data_tx.setter
    def feature_data_tx(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_tx, value)

    @staticmethod
    def check_acc_offset_range(value: int) -> None:
        if not (-256 <= value <= 255):
            error_msg = f"Value {value} outside of supported range [-256; 255]"
            raise NotImplementedError(error_msg)

    @staticmethod
    def convert_signed_bytes(byte_0: int, byte_1: int) -> int:
        raw_value = (byte_1 & 0x01) << 8 | byte_0
        if raw_value > 255:
            raw_value -= 512
        return raw_value

    @property
    def acc_offset_x(self) -> int:
        byte_0, byte_1 = self.read(BMA530Addr.acc_offset_0, 2)
        return self.convert_signed_bytes(byte_0, byte_1)

    @acc_offset_x.setter
    def acc_offset_x(self, value: int) -> None:
        self.check_acc_offset_range(value)
        byte_0, byte_1 = struct.pack("<h", value)
        self.write(BMA530Addr.acc_offset_0, byte_0)
        self.write(BMA530Addr.acc_offset_1, byte_1 & 0x01)

    @property
    def acc_offset_y(self) -> int:
        byte_0, byte_1 = self.read(BMA530Addr.acc_offset_2, 2)
        return self.convert_signed_bytes(byte_0, byte_1)

    @acc_offset_y.setter
    def acc_offset_y(self, value: int) -> None:
        self.check_acc_offset_range(value)
        byte_0, byte_1 = struct.pack("<h", value)
        self.write(BMA530Addr.acc_offset_2, byte_0)
        self.write(BMA530Addr.acc_offset_3, byte_1 & 0x01)

    @property
    def acc_offset_z(self) -> int:
        byte_0, byte_1 = self.read(BMA530Addr.acc_offset_4, 2)
        return self.convert_signed_bytes(byte_0, byte_1)

    @acc_offset_z.setter
    def acc_offset_z(self, value: int) -> None:
        self.check_acc_offset_range(value)
        byte_0, byte_1 = struct.pack("<h", value)
        self.write(BMA530Addr.acc_offset_4, byte_0)
        self.write(BMA530Addr.acc_offset_5, byte_1 & 0x01)

    @property
    def acc_self_test(self) -> int:
        return self.read(BMA530Addr.acc_self_test)

    @acc_self_test.setter
    def acc_self_test(self, value: int) -> None:
        self.write(BMA530Addr.acc_self_test, value)

    def cmd(self, value: int) -> None:
        self.write(BMA530Addr.cmd, value)

    cmd = property(None, cmd)

    def read_extended_register(self) -> int:
        payload = self.read(BMA530Addr.feature_data_tx, 4)
        (register_value,) = struct.unpack("<H", payload[2:])
        return register_value

    def write_extended_register(self, value: int) -> None:
        byte_0, byte_1 = struct.pack("<H", value)
        self.write(BMA530Addr.feature_data_tx, array("B", (byte_0, byte_1)))

    @property
    def feat_conf_err(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.feat_conf_err.value)
        return self.read_extended_register()

    @feat_conf_err.setter
    def feat_conf_err(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.feat_conf_err.value)
        self.write_extended_register(value)

    @property
    def general_settings_0(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.general_settings_0.value)
        return self.read_extended_register()

    @general_settings_0.setter
    def general_settings_0(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.general_settings_0.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt1_1(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_1.value)
        return self.read_extended_register()

    @generic_interrupt1_1.setter
    def generic_interrupt1_1(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_1.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt1_2(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_2.value)
        return self.read_extended_register()

    @generic_interrupt1_2.setter
    def generic_interrupt1_2(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_2.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt1_3(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_3.value)
        return self.read_extended_register()

    @generic_interrupt1_3.setter
    def generic_interrupt1_3(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_3.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt1_4(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_4.value)
        return self.read_extended_register()

    @generic_interrupt1_4.setter
    def generic_interrupt1_4(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_4.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt1_5(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_5.value)
        return self.read_extended_register()

    @generic_interrupt1_5.setter
    def generic_interrupt1_5(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_5.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt1_6(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_6.value)
        return self.read_extended_register()

    @generic_interrupt1_6.setter
    def generic_interrupt1_6(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_6.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt1_7(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_7.value)
        return self.read_extended_register()

    @generic_interrupt1_7.setter
    def generic_interrupt1_7(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt1_7.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt2_1(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_1.value)
        return self.read_extended_register()

    @generic_interrupt2_1.setter
    def generic_interrupt2_1(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_1.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt2_2(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_2.value)
        return self.read_extended_register()

    @generic_interrupt2_2.setter
    def generic_interrupt2_2(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_2.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt2_3(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_3.value)
        return self.read_extended_register()

    @generic_interrupt2_3.setter
    def generic_interrupt2_3(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_3.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt2_4(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_4.value)
        return self.read_extended_register()

    @generic_interrupt2_4.setter
    def generic_interrupt2_4(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_4.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt2_5(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_5.value)
        return self.read_extended_register()

    @generic_interrupt2_5.setter
    def generic_interrupt2_5(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_5.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt2_6(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_6.value)
        return self.read_extended_register()

    @generic_interrupt2_6.setter
    def generic_interrupt2_6(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_6.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt2_7(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_7.value)
        return self.read_extended_register()

    @generic_interrupt2_7.setter
    def generic_interrupt2_7(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt2_7.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt3_1(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_1.value)
        return self.read_extended_register()

    @generic_interrupt3_1.setter
    def generic_interrupt3_1(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_1.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt3_2(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_2.value)
        return self.read_extended_register()

    @generic_interrupt3_2.setter
    def generic_interrupt3_2(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_2.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt3_3(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_3.value)
        return self.read_extended_register()

    @generic_interrupt3_3.setter
    def generic_interrupt3_3(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_3.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt3_4(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_4.value)
        return self.read_extended_register()

    @generic_interrupt3_4.setter
    def generic_interrupt3_4(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_4.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt3_5(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_5.value)
        return self.read_extended_register()

    @generic_interrupt3_5.setter
    def generic_interrupt3_5(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_5.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt3_6(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_6.value)
        return self.read_extended_register()

    @generic_interrupt3_6.setter
    def generic_interrupt3_6(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_6.value)
        self.write_extended_register(value)

    @property
    def generic_interrupt3_7(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_7.value)
        return self.read_extended_register()

    @generic_interrupt3_7.setter
    def generic_interrupt3_7(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.generic_interrupt3_7.value)
        self.write_extended_register(value)

    @property
    def step_counter(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.step_counter.value)
        return self.read_extended_register()

    @step_counter.setter
    def step_counter(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.step_counter.value)
        self.write_extended_register(value)

    @property
    def sig_motion(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.sig_motion.value)
        return self.read_extended_register()

    @sig_motion.setter
    def sig_motion(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.sig_motion.value)
        self.write_extended_register(value)

    @property
    def tilt_1(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.tilt_1.value)
        return self.read_extended_register()

    @tilt_1.setter
    def tilt_1(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.tilt_1.value)
        self.write_extended_register(value)

    @property
    def tilt_2(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.tilt_2.value)
        return self.read_extended_register()

    @tilt_2.setter
    def tilt_2(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.tilt_2.value)
        self.write_extended_register(value)

    @property
    def orientation_1(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.orientation_1.value)
        return self.read_extended_register()

    @orientation_1.setter
    def orientation_1(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.orientation_1.value)
        self.write_extended_register(value)

    @property
    def orientation_2(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.orientation_2.value)
        return self.read_extended_register()

    @orientation_2.setter
    def orientation_2(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.orientation_2.value)
        self.write_extended_register(value)

    @property
    def foc_0(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.foc_0.value)
        return self.read_extended_register()

    @foc_0.setter
    def foc_0(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.foc_0.value)
        self.write_extended_register(value)

    @property
    def foc_1(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.foc_1.value)
        return self.read_extended_register()

    @foc_1.setter
    def foc_1(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.foc_1.value)
        self.write_extended_register(value)

    @property
    def foc_2(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.foc_2.value)
        return self.read_extended_register()

    @foc_2.setter
    def foc_2(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.foc_2.value)
        self.write_extended_register(value)

    @property
    def foc_3(self) -> int:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.foc_3.value)
        return self.read_extended_register()

    @foc_3.setter
    def foc_3(self, value: int) -> None:
        self.write(BMA530Addr.feature_data_addr, BMA530ExtendedAddr.foc_3.value)
        self.write_extended_register(value)
