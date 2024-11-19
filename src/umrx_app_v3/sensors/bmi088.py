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
    def gyro_rate_x(self) -> int:
        lsb = self.read_gyro(BMI088.gyro_rate_x_lsb_addr)
        msb = self.read_gyro(BMI088.gyro_rate_x_msb_addr)
        return (msb << 8) | lsb

    @property
    def gyro_rate_y(self) -> int:
        lsb = self.read_gyro(BMI088.gyro_rate_y_lsb_addr)
        msb = self.read_gyro(BMI088.gyro_rate_y_msb_addr)
        return (msb << 8) | lsb

    @property
    def gyro_rate_z(self) -> int:
        lsb = self.read_gyro(BMI088.gyro_rate_z_lsb_addr)
        msb = self.read_gyro(BMI088.gyro_rate_z_msb_addr)
        return (msb << 8) | lsb

    @property
    def gyro_int_stat_1(self) -> int:
        return self.read_gyro(BMI088.gyro_int_stat_1_addr)

    @property
    def gyro_fifo_status(self) -> int:
        return self.read_gyro(BMI088.gyro_fifo_status_addr)

    @property
    def gyro_lpm1(self) -> int:
        return self.read_gyro(BMI088.gyro_lpm1_addr)

    @gyro_lpm1.setter
    def gyro_lpm1(self, value: int) -> None:
        self.write_gyro(BMI088.gyro_lpm1_addr, value)
