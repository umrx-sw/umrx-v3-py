import struct
from collections.abc import Callable
from enum import Enum


class BMI088GyroAddr(Enum):
    gyro_chip_id = 0x00
    gyro_rate_x_lsb = 0x02
    gyro_rate_x_msb = 0x03
    gyro_rate_y_lsb = 0x04
    gyro_rate_y_msb = 0x05
    gyro_rate_z_lsb = 0x06
    gyro_rate_z_msb = 0x07
    gyro_int_stat_1 = 0x0A
    gyro_fifo_status = 0x0E
    gyro_range = 0x0F
    gyro_bandwidth = 0x10
    gyro_lpm1 = 0x11
    gyro_soft_reset = 0x14
    gyro_int_ctrl = 0x15
    gyro_int3_int4_io_conf = 0x16
    gyro_int3_int4_io_map = 0x18
    gyro_fifo_wm_en = 0x1E
    gyro_fifo_ext_int_s = 0x34
    gyro_self_test = 0x3C
    gyro_fifo_config_0 = 0x3D
    gyro_fifo_config_1 = 0x3E
    gyro_fifo_data = 0x3F


class BMI088AccelAddr(Enum):
    acc_chip_id = 0x00
    acc_err_reg = 0x02
    acc_status = 0x03
    acc_x_lsb = 0x12
    acc_x_msb = 0x13
    acc_y_lsb = 0x14
    acc_y_msb = 0x15
    acc_z_lsb = 0x16
    acc_z_msb = 0x17
    acc_sensor_time_0 = 0x18
    acc_sensor_time_1 = 0x19
    acc_sensor_time_2 = 0x1A
    acc_int_stat_1 = 0x1D
    acc_temp_msb = 0x22
    acc_temp_lsb = 0x23
    acc_fifo_length_0 = 0x24
    acc_fifo_length_1 = 0x25
    acc_fifo_data = 0x26
    acc_conf = 0x40
    acc_range = 0x41
    acc_fifo_downs = 0x45
    acc_fifo_wtm_0 = 0x46
    acc_fifo_wtm_1 = 0x47
    acc_fifo_config_0 = 0x48
    acc_fifo_config_1 = 0x49
    acc_int1_io_ctrl = 0x53
    acc_int2_io_ctrl = 0x54
    acc_int_map_data = 0x58
    acc_self_test = 0x6D
    acc_pwr_conf = 0x7C
    acc_pwr_ctrl = 0x7D
    acc_soft_reset = 0x7E


class BMI088:
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
        return self.read_gyro(BMI088GyroAddr.gyro_chip_id)

    @property
    def gyro_rate(self) -> tuple[int, int, int]:
        payload = self.read_gyro(BMI088GyroAddr.gyro_rate_x_lsb, 6)
        g_x, g_y, g_z = struct.unpack("<hhh", payload)
        return g_x, g_y, g_z

    @property
    def gyro_int_stat_1(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_int_stat_1)

    @property
    def gyro_fifo_status(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_fifo_status)

    @property
    def gyro_range(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_range)

    @gyro_range.setter
    def gyro_range(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_range, value)

    @property
    def gyro_bandwidth(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_bandwidth)

    @gyro_bandwidth.setter
    def gyro_bandwidth(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_bandwidth, value)

    @property
    def gyro_lpm1(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_lpm1)

    @gyro_lpm1.setter
    def gyro_lpm1(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_lpm1, value)

    def gyro_soft_reset(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_soft_reset, value)

    gyro_soft_reset = property(None, gyro_soft_reset)

    @property
    def gyro_int_ctrl(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_int_ctrl)

    @gyro_int_ctrl.setter
    def gyro_int_ctrl(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_int_ctrl, value)

    @property
    def gyro_int3_int4_io_conf(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_int3_int4_io_conf)

    @gyro_int3_int4_io_conf.setter
    def gyro_int3_int4_io_conf(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_int3_int4_io_conf, value)

    @property
    def gyro_int3_int4_io_map(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_int3_int4_io_map)

    @gyro_int3_int4_io_map.setter
    def gyro_int3_int4_io_map(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_int3_int4_io_map, value)

    @property
    def gyro_fifo_wm_en(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_fifo_wm_en)

    @gyro_fifo_wm_en.setter
    def gyro_fifo_wm_en(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_fifo_wm_en, value)

    @property
    def gyro_fifo_ext_int_s(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_fifo_ext_int_s)

    @gyro_fifo_ext_int_s.setter
    def gyro_fifo_ext_int_s(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_fifo_ext_int_s, value)

    @property
    def gyro_self_test(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_self_test)

    @gyro_self_test.setter
    def gyro_self_test(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_self_test, value)

    @property
    def gyro_fifo_config_0(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_fifo_config_0)

    @gyro_fifo_config_0.setter
    def gyro_fifo_config_0(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_fifo_config_0, value)

    @property
    def gyro_fifo_config_1(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_fifo_config_1)

    @gyro_fifo_config_1.setter
    def gyro_fifo_config_1(self, value: int) -> None:
        self.write_gyro(BMI088GyroAddr.gyro_fifo_config_1, value)

    @property
    def gyro_fifo_data(self) -> int:
        return self.read_gyro(BMI088GyroAddr.gyro_fifo_data)

    # Accelerometer
    @property
    def acc_chip_id(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_chip_id)

    @property
    def acc_err_reg(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_err_reg)

    @property
    def acc_status(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_status)

    @property
    def acceleration(self) -> tuple[int, int, int]:
        payload = self.read_accel(BMI088AccelAddr.acc_x_lsb, 6)
        a_x, a_y, a_z = struct.unpack("<hhh", payload)
        return a_x, a_y, a_z

    @property
    def acc_sensor_time(self) -> int:
        byte_0, byte_1, byte_2 = self.read_accel(BMI088AccelAddr.acc_sensor_time_0, 3)
        return (byte_2 << 16) | (byte_1 << 8) | byte_0

    @property
    def acc_int_stat_1(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_int_stat_1)

    @property
    def acc_temperature(self) -> int:
        msb, lsb = self.read_accel(BMI088AccelAddr.acc_temp_msb, 2)
        return (msb << 3) | (lsb >> 5)

    @property
    def acc_fifo_length_0(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_fifo_length_0)

    @property
    def acc_fifo_length_1(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_fifo_length_1)

    @property
    def acc_fifo_data(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_fifo_data)

    @property
    def acc_conf(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_conf)

    @acc_conf.setter
    def acc_conf(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_conf, value)

    @property
    def acc_range(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_range)

    @acc_range.setter
    def acc_range(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_range, value)

    @property
    def acc_fifo_downs(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_fifo_downs)

    @acc_fifo_downs.setter
    def acc_fifo_downs(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_fifo_downs, value)

    @property
    def acc_fifo_wtm_0(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_fifo_wtm_0)

    @acc_fifo_wtm_0.setter
    def acc_fifo_wtm_0(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_fifo_wtm_0, value)

    @property
    def acc_fifo_wtm_1(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_fifo_wtm_1)

    @acc_fifo_wtm_1.setter
    def acc_fifo_wtm_1(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_fifo_wtm_1, value)

    @property
    def acc_fifo_config_0(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_fifo_config_0)

    @acc_fifo_config_0.setter
    def acc_fifo_config_0(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_fifo_config_0, value)

    @property
    def acc_fifo_config_1(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_fifo_config_1)

    @acc_fifo_config_1.setter
    def acc_fifo_config_1(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_fifo_config_1, value)

    @property
    def acc_int1_io_ctrl(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_int1_io_ctrl)

    @acc_int1_io_ctrl.setter
    def acc_int1_io_ctrl(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_int1_io_ctrl, value)

    @property
    def acc_int2_io_ctrl(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_int2_io_ctrl)

    @acc_int2_io_ctrl.setter
    def acc_int2_io_ctrl(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_int2_io_ctrl, value)

    @property
    def acc_int_map_data(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_int_map_data)

    @acc_int_map_data.setter
    def acc_int_map_data(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_int_map_data, value)

    @property
    def acc_self_test(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_self_test)

    @acc_self_test.setter
    def acc_self_test(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_self_test, value)

    @property
    def acc_pwr_conf(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_pwr_conf)

    @acc_pwr_conf.setter
    def acc_pwr_conf(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_pwr_conf, value)

    @property
    def acc_pwr_ctrl(self) -> int:
        return self.read_accel(BMI088AccelAddr.acc_pwr_ctrl)

    @acc_pwr_ctrl.setter
    def acc_pwr_ctrl(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_pwr_ctrl, value)

    def acc_soft_reset(self, value: int) -> None:
        self.write_accel(BMI088AccelAddr.acc_soft_reset, value)

    acc_soft_reset = property(None, acc_soft_reset)
