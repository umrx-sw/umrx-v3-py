import struct
from collections.abc import Callable


class BMI088:
    gyro_chip_id_addr = 0x00
    gyro_rate_x_lsb_addr = 0x02
    gyro_rate_x_msb_addr = 0x03
    gyro_rate_y_lsb_addr = 0x04
    gyro_rate_y_msb_addr = 0x05
    gyro_rate_z_lsb_addr = 0x06
    gyro_rate_z_msb_addr = 0x07
    gyro_int_stat_1_addr = 0x0A
    gyro_fifo_status_addr = 0x0E
    gyro_range_addr = 0x0F
    gyro_bandwidth_addr = 0x10
    gyro_lpm1_addr = 0x11
    gyro_soft_reset_addr = 0x14
    gyro_int_ctrl_addr = 0x15
    gyro_int3_int4_io_conf_addr = 0x16
    gyro_int3_int4_io_map_addr = 0x18
    gyro_fifo_wm_en_addr = 0x1E
    gyro_fifo_ext_int_s_addr = 0x34
    gyro_self_test_addr = 0x3C
    gyro_fifo_config_0_addr = 0x3D
    gyro_fifo_config_1_addr = 0x3E
    gyro_fifo_data_addr = 0x3F

    acc_chip_id_addr = 0x00
    acc_err_reg_addr = 0x02
    acc_status_addr = 0x03
    acc_x_lsb_addr = 0x12
    acc_x_msb_addr = 0x13
    acc_y_lsb_addr = 0x14
    acc_y_msb_addr = 0x15
    acc_z_lsb_addr = 0x16
    acc_z_msb_addr = 0x17
    acc_sensor_time_0_addr = 0x18
    acc_sensor_time_1_addr = 0x19
    acc_sensor_time_2_addr = 0x1A
    acc_int_stat_1_addr = 0x1D
    acc_temp_msb_addr = 0x22
    acc_temp_lsb_addr = 0x23
    acc_fifo_length_0_addr = 0x24
    acc_fifo_length_1_addr = 0x25
    acc_fifo_data_addr = 0x26
    acc_conf_addr = 0x40
    acc_range_addr = 0x41
    acc_fifo_downs_addr = 0x45
    acc_fifo_wtm_0_addr = 0x46
    acc_fifo_wtm_1_addr = 0x47
    acc_fifo_config_0_addr = 0x48
    acc_fifo_config_1_addr = 0x49
    acc_int1_io_ctrl_addr = 0x53
    acc_int2_io_ctrl_addr = 0x54
    acc_int_map_data_addr = 0x58
    acc_self_test_addr = 0x6D
    acc_pwr_conf_addr = 0x7C
    acc_pwr_ctrl_addr = 0x7D
    acc_soft_reset_addr = 0x7E

    def __init__(self) -> None:
        self.read_gyro: Callable | None = None
        self.write_gyro: Callable | None = None
        self.read_accel: Callable | None = None
        self.write_accel: Callable | None = None

    def assign_gyro_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read_gyro = read_callback
        self.write_gyro = write_callback

    def assign_accel_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read_accel = read_callback
        self.write_accel = write_callback

    @property
    def gyro_chip_id(self) -> int:
        return self.read_gyro(BMI088.gyro_chip_id_addr)

    @property
    def gyro_rate(self) -> tuple[int, int, int]:
        payload = self.read_gyro(BMI088.gyro_rate_x_lsb_addr, 6)
        g_x, g_y, g_z = struct.unpack("<hhh", payload)
        return g_x, g_y, g_z

    @property
    def gyro_int_stat_1(self) -> int:
        return self.read_gyro(BMI088.gyro_int_stat_1_addr)

    @property
    def gyro_fifo_status(self) -> int:
        return self.read_gyro(BMI088.gyro_fifo_status_addr)

    @property
    def gyro_range(self) -> int:
        return self.read_gyro(BMI088.gyro_range_addr)

    @gyro_range.setter
    def gyro_range(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_range_addr, value)

    @property
    def gyro_bandwidth(self) -> int:
        return self.read_gyro(BMI088.gyro_bandwidth_addr)

    @gyro_bandwidth.setter
    def gyro_bandwidth(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_bandwidth_addr, value)

    @property
    def gyro_lpm1(self) -> int:
        return self.read_gyro(BMI088.gyro_lpm1_addr)

    @gyro_lpm1.setter
    def gyro_lpm1(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_lpm1_addr, value)

    def gyro_soft_reset(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_soft_reset_addr, value)

    gyro_soft_reset = property(None, gyro_soft_reset)

    @property
    def gyro_int_ctrl(self) -> int:
        return self.read_gyro(BMI088.gyro_int_ctrl_addr)

    @gyro_int_ctrl.setter
    def gyro_int_ctrl(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_int_ctrl_addr, value)

    @property
    def gyro_int3_int4_io_conf(self) -> int:
        return self.read_gyro(BMI088.gyro_int3_int4_io_conf_addr)

    @gyro_int3_int4_io_conf.setter
    def gyro_int3_int4_io_conf(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_int3_int4_io_conf_addr, value)

    @property
    def gyro_int3_int4_io_map(self) -> int:
        return self.read_gyro(BMI088.gyro_int3_int4_io_map_addr)

    @gyro_int3_int4_io_map.setter
    def gyro_int3_int4_io_map(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_int3_int4_io_map_addr, value)

    @property
    def gyro_fifo_wm_en(self) -> int:
        return self.read_gyro(BMI088.gyro_fifo_wm_en_addr)

    @gyro_fifo_wm_en.setter
    def gyro_fifo_wm_en(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_fifo_wm_en_addr, value)

    @property
    def gyro_fifo_ext_int_s(self) -> int:
        return self.read_gyro(BMI088.gyro_fifo_ext_int_s_addr)

    @gyro_fifo_ext_int_s.setter
    def gyro_fifo_ext_int_s(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_fifo_ext_int_s_addr, value)

    @property
    def gyro_self_test(self) -> int:
        return self.read_gyro(BMI088.gyro_self_test_addr)

    @gyro_self_test.setter
    def gyro_self_test(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_self_test_addr, value)

    @property
    def gyro_fifo_config_0(self) -> int:
        return self.read_gyro(BMI088.gyro_fifo_config_0_addr)

    @gyro_fifo_config_0.setter
    def gyro_fifo_config_0(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_fifo_config_0_addr, value)

    @property
    def gyro_fifo_config_1(self) -> int:
        return self.read_gyro(BMI088.gyro_fifo_config_1_addr)

    @gyro_fifo_config_1.setter
    def gyro_fifo_config_1(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_fifo_config_1_addr, value)

    @property
    def gyro_fifo_data(self) -> int:
        return self.read_gyro(BMI088.gyro_fifo_data_addr)

    # Accelerometer
    @property
    def acc_chip_id(self) -> int:
        return self.read_accel(BMI088.acc_chip_id_addr)

    @property
    def acc_err_reg(self) -> int:
        return self.read_accel(BMI088.acc_err_reg_addr)

    @property
    def acc_status(self) -> int:
        return self.read_accel(BMI088.acc_status_addr)

    @property
    def acceleration(self) -> tuple[int, int, int]:
        payload = self.read_accel(BMI088.acc_x_lsb_addr, 6)
        a_x, a_y, a_z = struct.unpack("<hhh", payload)
        return a_x, a_y, a_z

    @property
    def acc_sensor_time(self) -> int:
        byte_0, byte_1, byte_2 = self.read_accel(BMI088.acc_sensor_time_0_addr, 3)
        return (byte_2 << 16) | (byte_1 << 8) | byte_0

    @property
    def acc_int_stat_1(self) -> int:
        return self.read_accel(BMI088.acc_int_stat_1_addr)

    @property
    def acc_temperature(self) -> int:
        msb, lsb = self.read_accel(BMI088.acc_temp_msb_addr, 2)
        return (msb << 3) | (lsb >> 5)

    @property
    def acc_fifo_length_0(self) -> int:
        return self.read_accel(BMI088.acc_fifo_length_0_addr)

    @property
    def acc_fifo_length_1(self) -> int:
        return self.read_accel(BMI088.acc_fifo_length_1_addr)

    @property
    def acc_fifo_data(self) -> int:
        return self.read_accel(BMI088.acc_fifo_data_addr)

    @property
    def acc_conf(self) -> int:
        return self.read_accel(BMI088.acc_conf_addr)

    @acc_conf.setter
    def acc_conf(self, value: int) -> None:
        self.write_accel(BMI088.acc_conf_addr, value)

    @property
    def acc_range(self) -> int:
        return self.read_accel(BMI088.acc_range_addr)

    @acc_range.setter
    def acc_range(self, value: int) -> None:
        self.write_accel(BMI088.acc_range_addr, value)

    @property
    def acc_fifo_downs(self) -> int:
        return self.read_accel(BMI088.acc_fifo_downs_addr)

    @acc_fifo_downs.setter
    def acc_fifo_downs(self, value: int) -> None:
        self.write_accel(BMI088.acc_fifo_downs_addr, value)

    @property
    def acc_fifo_wtm_0(self) -> int:
        return self.read_accel(BMI088.acc_fifo_wtm_0_addr)

    @acc_fifo_wtm_0.setter
    def acc_fifo_wtm_0(self, value: int) -> None:
        self.write_accel(BMI088.acc_fifo_wtm_0_addr, value)

    @property
    def acc_fifo_wtm_1(self) -> int:
        return self.read_accel(BMI088.acc_fifo_wtm_1_addr)

    @acc_fifo_wtm_1.setter
    def acc_fifo_wtm_1(self, value: int) -> None:
        self.write_accel(BMI088.acc_fifo_wtm_1_addr, value)

    @property
    def acc_fifo_config_0(self) -> int:
        return self.read_accel(BMI088.acc_fifo_config_0_addr)

    @acc_fifo_config_0.setter
    def acc_fifo_config_0(self, value: int) -> None:
        self.write_accel(BMI088.acc_fifo_config_0_addr, value)

    @property
    def acc_fifo_config_1(self) -> int:
        return self.read_accel(BMI088.acc_fifo_config_1_addr)

    @acc_fifo_config_1.setter
    def acc_fifo_config_1(self, value: int) -> None:
        self.write_accel(BMI088.acc_fifo_config_1_addr, value)

    @property
    def acc_int1_io_ctrl(self) -> int:
        return self.read_accel(BMI088.acc_int1_io_ctrl_addr)

    @acc_int1_io_ctrl.setter
    def acc_int1_io_ctrl(self, value: int) -> None:
        self.write_accel(BMI088.acc_int1_io_ctrl_addr, value)

    @property
    def acc_int2_io_ctrl(self) -> int:
        return self.read_accel(BMI088.acc_int2_io_ctrl_addr)

    @acc_int2_io_ctrl.setter
    def acc_int2_io_ctrl(self, value: int) -> None:
        self.write_accel(BMI088.acc_int2_io_ctrl_addr, value)

    @property
    def acc_int_map_data(self) -> int:
        return self.read_accel(BMI088.acc_int_map_data_addr)

    @acc_int_map_data.setter
    def acc_int_map_data(self, value: int) -> None:
        self.write_accel(BMI088.acc_int_map_data_addr, value)

    @property
    def acc_self_test(self) -> int:
        return self.read_accel(BMI088.acc_self_test_addr)

    @acc_self_test.setter
    def acc_self_test(self, value: int) -> None:
        self.write_accel(BMI088.acc_self_test_addr, value)

    @property
    def acc_pwr_conf(self) -> int:
        return self.read_accel(BMI088.acc_pwr_conf_addr)

    @acc_pwr_conf.setter
    def acc_pwr_conf(self, value: int) -> None:
        self.write_accel(BMI088.acc_pwr_conf_addr, value)

    @property
    def acc_pwr_ctrl(self) -> int:
        return self.read_accel(BMI088.acc_pwr_ctrl_addr)

    @acc_pwr_ctrl.setter
    def acc_pwr_ctrl(self, value: int) -> None:
        self.write_accel(BMI088.acc_pwr_ctrl_addr, value)

    def acc_soft_reset(self, value: int) -> None:
        self.write_accel(BMI088.acc_soft_reset_addr, value)

    acc_soft_reset = property(None, acc_soft_reset)
