import struct
from collections.abc import Callable
from enum import Enum
from functools import cached_property


class BMM350Addr(Enum):
    chip_id = 0x00
    err_reg = 0x02
    pad_ctrl = 0x03
    pmu_cmd_aggr_set = 0x04
    pmu_cmd_axis_en = 0x05
    pmu_cmd = 0x06
    pmu_cmd_status_0 = 0x07
    pmu_cmd_status_1 = 0x08
    i3c_err = 0x09
    i2c_wdt_set = 0x0A
    transducer_rev_id = 0x0D
    sensor_time_2 = 0x0C
    int_ctrl = 0x2E
    int_ctrl_ibi = 0x2F
    int_status = 0x30
    mag_x_xlsb = 0x31
    mag_x_lsb = 0x32
    mag_x_msb = 0x33
    mag_y_xlsb = 0x34
    mag_y_lsb = 0x35
    mag_y_msb = 0x36
    mag_z_xlsb = 0x37
    mag_z_lsb = 0x38
    mag_z_msb = 0x39
    temp_xlsb = 0x3A
    temp_lsb = 0x3B
    temp_msb = 0x3C
    sensor_time_xlsb = 0x3D
    sensor_time_lsb = 0x3E
    sensor_time_msb = 0x3F
    otp_cmd_reg = 0x50
    otp_data_msb_reg = 0x52
    otp_data_lsb_reg = 0x53
    otp_status_reg = 0x55
    tmr_selftest_user = 0x60
    ctrl_user = 0x61
    cmd = 0x7E


class BMM350OtpAddr(Enum):
    temp_off_sens = 0x0D
    mag_offset_x = 0x0E
    mag_offset_y = 0x0F
    mag_offset_z = 0x10
    mag_sens_x = 0x10  # noqa: PIE796
    mag_sens_y = 0x11
    mag_sens_z = 0x11  # noqa: PIE796
    mag_tco_x = 0x12
    mag_tco_y = 0x13
    mag_tco_z = 0x14
    mag_tcs_x = 0x12  # noqa: PIE796
    mag_tcs_y = 0x13  # noqa: PIE796
    mag_tcs_z = 0x14  # noqa: PIE796
    mag_dut_t_0 = 0x18
    cross_x_y = 0x15
    cross_y_x = 0x15  # noqa: PIE796
    cross_z_x = 0x16
    cross_z_y = 0x16  # noqa: PIE796


class BMM350Error(Exception): ...


class BMM350:
    def __init__(self) -> None:
        self.read: Callable | None = None
        self.write: Callable | None = None

    def assign_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read = read_callback
        self.write = write_callback

    @staticmethod
    def sign_convert_8_bit(value: int) -> int:
        (signed_value,) = struct.unpack("<b", int.to_bytes(value, 1, byteorder="little"))
        return signed_value

    @staticmethod
    def sign_convert_12_bit(value: int) -> int:
        if value > 2**11 - 1:
            value -= 2**12
        return value

    @staticmethod
    def sign_convert_16_bit(value: int) -> int:
        if value > 2**15 - 1:
            value -= 2**16
        return value

    @staticmethod
    def sign_convert_24_bit(value: int) -> int:
        if value > 2**23 - 1:
            value -= 2**24
        return value

    @staticmethod
    def sign_convert_magnetometer(m_x: int, m_y: int, m_z: int) -> tuple[int, int, int]:
        m_x_signed = BMM350.sign_convert_24_bit(m_x)
        m_y_signed = BMM350.sign_convert_24_bit(m_y)
        m_z_signed = BMM350.sign_convert_24_bit(m_z)
        return m_x_signed, m_y_signed, m_z_signed

    @property
    def chip_id(self) -> int:
        return self.read(BMM350Addr.chip_id)

    @property
    def err_reg(self) -> int:
        return self.read(BMM350Addr.err_reg)

    @err_reg.setter
    def err_reg(self, value: int) -> None:
        self.write(BMM350Addr.err_reg, value)

    @property
    def pad_ctrl(self) -> int:
        return self.read(BMM350Addr.pad_ctrl)

    @pad_ctrl.setter
    def pad_ctrl(self, value: int) -> None:
        self.write(BMM350Addr.pad_ctrl, value)

    @property
    def pmu_cmd_aggr_set(self) -> int:
        return self.read(BMM350Addr.pmu_cmd_aggr_set)

    @pmu_cmd_aggr_set.setter
    def pmu_cmd_aggr_set(self, value: int) -> None:
        self.write(BMM350Addr.pmu_cmd_aggr_set, value)

    @property
    def pmu_cmd_axis_en(self) -> int:
        return self.read(BMM350Addr.pmu_cmd_axis_en)

    @pmu_cmd_axis_en.setter
    def pmu_cmd_axis_en(self, value: int) -> None:
        self.write(BMM350Addr.pmu_cmd_axis_en, value)

    def pmu_cmd(self, value: int) -> None:
        self.write(BMM350Addr.pmu_cmd, value)

    pmu_cmd = property(None, pmu_cmd)

    @property
    def pmu_cmd_status_0(self) -> int:
        return self.read(BMM350Addr.pmu_cmd_status_0)

    @property
    def pmu_cmd_status_1(self) -> int:
        return self.read(BMM350Addr.pmu_cmd_status_1)

    @property
    def i3c_err(self) -> int:
        return self.read(BMM350Addr.i3c_err)

    @i3c_err.setter
    def i3c_err(self, value: int) -> None:
        self.write(BMM350Addr.i3c_err, value)

    @property
    def i2c_wdt_set(self) -> int:
        return self.read(BMM350Addr.i2c_wdt_set)

    @i2c_wdt_set.setter
    def i2c_wdt_set(self, value: int) -> None:
        self.write(BMM350Addr.i2c_wdt_set, value)

    @property
    def transducer_rev_id(self) -> int:
        return self.read(BMM350Addr.transducer_rev_id)

    @property
    def int_ctrl(self) -> int:
        return self.read(BMM350Addr.int_ctrl)

    @int_ctrl.setter
    def int_ctrl(self, value: int) -> None:
        self.write(BMM350Addr.int_ctrl, value)

    @property
    def int_ctrl_ibi(self) -> int:
        return self.read(BMM350Addr.int_ctrl_ibi)

    @int_ctrl_ibi.setter
    def int_ctrl_ibi(self, value: int) -> None:
        self.write(BMM350Addr.int_ctrl_ibi, value)

    @property
    def int_status(self) -> int:
        return self.read(BMM350Addr.int_status)

    @int_status.setter
    def int_status(self, value: int) -> None:
        self.write(BMM350Addr.int_status, value)

    @property
    def magnetometer_raw(self) -> tuple[int, int, int]:
        x_xlsb, x_lsb, x_msb, y_xlsb, y_lsb, y_msb, z_xlsb, z_lsb, z_msb = self.read(BMM350Addr.mag_x_xlsb, 9)
        m_x = (x_msb << 16) | (x_lsb << 8) | x_xlsb
        m_y = (y_msb << 16) | (y_lsb << 8) | y_xlsb
        m_z = (z_msb << 16) | (z_lsb << 8) | z_msb
        m_x, m_y, m_z = BMM350.sign_convert_magnetometer(m_x, m_y, m_z)
        return m_x, m_y, m_z

    @property
    def temperature_raw(self) -> int:
        t_xlsb, t_lsb, t_msb = self.read(BMM350Addr.temp_xlsb, 3)
        temerature_raw = (t_msb << 16) | (t_lsb << 8) | t_xlsb
        return BMM350.sign_convert_24_bit(temerature_raw)

    @property
    def sensor_time(self) -> float:
        t_xlsb, t_lsb, t_msb = self.read(BMM350Addr.sensor_time_xlsb, 3)
        return ((t_msb << 16) | (t_lsb << 8) | t_xlsb) * 39.0625e-6

    @property
    def otp_cmd_reg(self) -> int:
        return self.read(BMM350Addr.otp_cmd_reg)

    @otp_cmd_reg.setter
    def otp_cmd_reg(self, value: int) -> None:
        self.write(BMM350Addr.otp_cmd_reg, value)

    @property
    def otp_data_msb_reg(self) -> int:
        return self.read(BMM350Addr.otp_data_msb_reg)

    @otp_data_msb_reg.setter
    def otp_data_msb_reg(self, value: int) -> None:
        self.write(BMM350Addr.otp_data_msb_reg, value)

    @property
    def otp_data_lsb_reg(self) -> int:
        return self.read(BMM350Addr.otp_data_lsb_reg)

    @otp_data_lsb_reg.setter
    def otp_data_lsb_reg(self, value: int) -> None:
        self.write(BMM350Addr.otp_data_lsb_reg, value)

    @property
    def otp_status_reg(self) -> int:
        return self.read(BMM350Addr.otp_status_reg)

    @property
    def tmr_selftest_user(self) -> int:
        return self.read(BMM350Addr.tmr_selftest_user)

    @tmr_selftest_user.setter
    def tmr_selftest_user(self, value: int) -> None:
        self.write(BMM350Addr.tmr_selftest_user, value)

    @property
    def ctrl_user(self) -> int:
        return self.read(BMM350Addr.ctrl_user)

    @ctrl_user.setter
    def ctrl_user(self, value: int) -> None:
        self.write(BMM350Addr.ctrl_user, value)

    def cmd(self, value: int) -> None:
        self.write(BMM350Addr.cmd, value)

    cmd = property(None, cmd)

    def read_otp_word(self, addr: BMM350OtpAddr) -> int:
        otp_read_cmd = 0x20 | (addr.value & 0x1F)
        self.otp_cmd_reg = otp_read_cmd
        status = self.otp_status_reg
        if (status & 0xE0) != 0:
            error_msg = f"BMM350 OTP status is not OK: got {status}"
            raise BMM350Error(error_msg)
        msb = self.otp_data_msb_reg
        lsb = self.otp_data_lsb_reg
        return (msb << 8) | lsb

    @cached_property
    def otp_temp_off_sens(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.temp_off_sens)

    @cached_property
    def otp_mag_offset_x(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_offset_x)

    @cached_property
    def otp_mag_offset_y(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_offset_y)

    @cached_property
    def otp_mag_offset_z(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_offset_z)

    @cached_property
    def otp_mag_sens_x(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_sens_x)

    @cached_property
    def otp_mag_sens_y(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_sens_y)

    @cached_property
    def otp_mag_sens_z(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_sens_z)

    @cached_property
    def otp_mag_tco_x(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_tco_x)

    @cached_property
    def otp_mag_tco_y(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_tco_y)

    @cached_property
    def otp_mag_tco_z(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_tco_z)

    @cached_property
    def otp_mag_tcs_x(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_tcs_x)

    @cached_property
    def otp_mag_tcs_y(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_tcs_y)

    @cached_property
    def otp_mag_tcs_z(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_tcs_z)

    @cached_property
    def otp_mag_dut_t_0(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.mag_dut_t_0)

    @cached_property
    def otp_cross_x_y(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.cross_x_y)

    @cached_property
    def otp_cross_y_x(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.cross_y_x)

    @cached_property
    def otp_cross_z_x(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.cross_z_x)

    @cached_property
    def otp_cross_z_y(self) -> int:
        return self.read_otp_word(BMM350OtpAddr.cross_z_y)

    @cached_property
    def offset_x(self) -> int:
        offset_x_val = self.otp_mag_offset_x & 0x0FFF
        return self.sign_convert_12_bit(offset_x_val)

    @cached_property
    def offset_y(self) -> int:
        offset_y_val = ((self.otp_mag_offset_x & 0xF000) >> 4) | (self.otp_mag_offset_y & 0x0FF)
        return self.sign_convert_12_bit(offset_y_val)

    @cached_property
    def offset_z(self) -> int:
        offset_z_val = (self.otp_mag_offset_y & 0x0F00) | (self.otp_mag_offset_z & 0x0FF)
        return self.sign_convert_12_bit(offset_z_val)

    @cached_property
    def t_offs(self) -> float:
        t_offs_val = self.otp_temp_off_sens & 0xFF
        return self.sign_convert_8_bit(t_offs_val) / 5.0

    @cached_property
    def sens_x(self) -> float:
        sens_x_val = (self.otp_mag_sens_x & 0xFF00) >> 8
        return self.sign_convert_8_bit(sens_x_val) / 256.0

    @cached_property
    def sens_y(self) -> float:
        sens_y_val = self.otp_mag_sens_y & 0x00FF
        return self.sign_convert_8_bit(sens_y_val) / 256.0 + 0.01

    @cached_property
    def sens_z(self) -> float:
        sens_z_val = (self.otp_mag_sens_z & 0xFF00) >> 8
        return self.sign_convert_8_bit(sens_z_val) / 256.0

    @cached_property
    def t_sens(self) -> float:
        t_sens_val = (self.otp_temp_off_sens & 0xFF00) >> 8
        return self.sign_convert_8_bit(t_sens_val) / 512.0

    @cached_property
    def tco_x(self) -> float:
        tco_x_val = self.otp_mag_tco_x & 0x00FF
        return self.sign_convert_8_bit(tco_x_val) / 32.0

    @cached_property
    def tco_y(self) -> float:
        tco_y_val = self.otp_mag_tco_y & 0x00FF
        return self.sign_convert_8_bit(tco_y_val) / 32.0

    @cached_property
    def tco_z(self) -> float:
        tco_z_val = self.otp_mag_tco_z & 0x00FF
        return self.sign_convert_8_bit(tco_z_val) / 32.0

    @cached_property
    def tcs_x(self) -> float:
        tcs_x_val = (self.otp_mag_tcs_x & 0xFF00) >> 8
        return self.sign_convert_8_bit(tcs_x_val) / 16384.0

    @cached_property
    def tcs_y(self) -> float:
        tcs_y_val = (self.otp_mag_tcs_y & 0xFF00) >> 8
        return self.sign_convert_8_bit(tcs_y_val) / 16384.0

    @cached_property
    def tcs_z(self) -> float:
        tcs_z_val = (self.otp_mag_tcs_z & 0xFF00) >> 8
        return self.sign_convert_8_bit(tcs_z_val) / 16384.0 - 0.0001

    @cached_property
    def dut_t0(self) -> float:
        return self.sign_convert_16_bit(self.otp_mag_dut_t_0) / 512.0 + 23.0

    @cached_property
    def cross_x_y(self) -> float:
        cross_x_y_val = self.otp_cross_x_y & 0x00FF
        return self.sign_convert_8_bit(cross_x_y_val) / 800.0

    @cached_property
    def cross_y_x(self) -> float:
        cross_y_x_val = (self.otp_cross_y_x & 0xFF00) >> 8
        return self.sign_convert_8_bit(cross_y_x_val) / 800.0

    @cached_property
    def cross_z_x(self) -> float:
        cross_z_x_val = self.otp_cross_z_x & 0x00FF
        return self.sign_convert_8_bit(cross_z_x_val) / 800.0

    @cached_property
    def cross_z_y(self) -> float:
        cross_z_y_val = (self.otp_cross_z_y & 0xFF00) >> 8
        return self.sign_convert_8_bit(cross_z_y_val) / 800.0

    @staticmethod
    def conversion_coefficients() -> tuple[float, float, float, float]:
        bxy_sens = 14.55
        bz_sens = 9.0
        temp_sens = 0.00204
        ina_xy_gain = 19.46
        ina_z_gain = 31.0
        adc_gain = 1 / 1.5
        lut_gain = 0.714607238769531
        power = 1000000.0 / 1048576.0
        magnetometer_x_coefficient = power / (bxy_sens * ina_xy_gain * adc_gain * lut_gain)
        magnetometer_y_coefficient = power / (bxy_sens * ina_xy_gain * adc_gain * lut_gain)
        magnetometer_z_coefficient = power / (bz_sens * ina_z_gain * adc_gain * lut_gain)
        temperature_coefficient = 1 / (temp_sens * adc_gain * lut_gain * 1048576)
        return (
            magnetometer_x_coefficient,
            magnetometer_y_coefficient,
            magnetometer_z_coefficient,
            temperature_coefficient,
        )

    @staticmethod
    def magnetometer_in_micro_tesla_uncompensated(
        m_x_raw: int, m_y_raw: int, m_z_raw: int
    ) -> tuple[float, float, float]:
        c_m_x, c_m_y, c_m_z, _ = BMM350.conversion_coefficients()
        return c_m_x * m_x_raw, c_m_y * m_y_raw, c_m_z * m_z_raw

    @staticmethod
    def temperature_in_degrees_uncompensated(temp_raw: int) -> float:
        _, _, _, temperature_coefficient = BMM350.conversion_coefficients()
        temperature_weighted = temp_raw * temperature_coefficient
        if temperature_weighted > 0:
            return temperature_weighted - 25.49
        if temperature_weighted < 0:
            return temperature_weighted + 25.49
        return 0.0

    def compensate_magnetometer_and_temperature(
        self, m_x_raw: int, m_y_raw: int, m_z_raw: int, temp_raw: int
    ) -> tuple[float, float, float, float]:
        m_x, m_y, m_z = BMM350.magnetometer_in_micro_tesla_uncompensated(m_x_raw, m_y_raw, m_z_raw)
        temp = BMM350.temperature_in_degrees_uncompensated(temp_raw)
        compensated_temperature = (1 + self.t_sens) * temp + self.t_offs

        comp_m_x = m_x * (1 + self.sens_x) + self.offset_x + self.tco_x * (compensated_temperature - self.dut_t0)
        comp_m_x /= 1 + self.tcs_x * (compensated_temperature - self.dut_t0)

        comp_m_y = m_y * (1 + self.sens_y) + self.offset_y + self.tco_y * (compensated_temperature - self.dut_t0)
        comp_m_y /= 1 + self.tcs_y * (compensated_temperature - self.dut_t0)

        comp_m_z = m_z * (1 + self.sens_z) + self.offset_z + self.tco_z * (compensated_temperature - self.dut_t0)
        comp_m_z /= 1 + self.tcs_z * (compensated_temperature - self.dut_t0)

        cross_m_x = (comp_m_x - self.cross_x_y * comp_m_y) / (1 - self.cross_y_x * self.cross_x_y)
        cross_m_y = (comp_m_y - self.cross_y_x * comp_m_x) / (1 - self.cross_x_y * self.cross_y_x)
        cross_m_z = comp_m_z + (
            comp_m_x * (self.cross_y_x * self.cross_z_y - self.cross_z_x)
            - comp_m_y * (self.cross_z_y - self.cross_x_y * self.cross_z_x)
        ) / (1 - self.cross_y_x * self.cross_x_y)

        return cross_m_x, cross_m_y, cross_m_z, compensated_temperature
