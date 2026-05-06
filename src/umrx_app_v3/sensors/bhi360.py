import struct
from collections.abc import Callable
from enum import Enum


class BHI360Addr(Enum):
    chan_cmd = 0x00
    chan_fifo_w = 0x01
    chan_fifo_nw = 0x02
    chan_status = 0x03
    chip_ctrl = 0x05
    host_interface_ctrl = 0x06
    host_interrupt_ctrl = 0x07
    reset_req = 0x14
    time_ev_req = 0x15
    host_ctrl = 0x16
    host_status = 0x17
    crc_0 = 0x18
    product_id = 0x1c
    revision_id = 0x1d
    rom_version_0 = 0x1e
    kernel_version_0 = 0x20
    user_version_0 = 0x22
    feature_status = 0x24
    boot_status = 0x25
    host_intr_time_0 = 0x26
    chip_id = 0x2b
    int_status = 0x2d
    error_value = 0x2e
    error_aux = 0x2f
    debug_value = 0x30
    debug_state = 0x31
    gp_5 = 0x32
    gp_6 = 0x36
    gp_7 = 0x3a


class BHI360CommandId(Enum):
    req_post_mortem_data = 0x0001
    upload_to_program_ram = 0x0002
    boot_program_ram = 0x0003
    set_inject_mode = 0x0007
    inject_data = 0x0008
    fifo_flush = 0x0009
    sw_passthrough = 0x000a
    req_self_test = 0x000b
    req_foc = 0x000c
    config_sensor = 0x000d
    change_range = 0x000e
    fifo_format_ctrl = 0x0015
    raise_host_inf_speed = 0x0017


class BHI360VirtualSensorId(Enum):
    acc_pass = 1
    acc_raw = 3
    acc = 4
    acc_bias = 5
    acc_wu = 6
    acc_raw_wu = 7
    si_accel = 8
    gyro_pass = 10
    gyro_raw = 12
    gyro = 13
    gyro_bias = 14
    gyro_wu = 15
    gyro_raw_wu = 16
    si_gyros = 17
    mag_pass = 19
    mag_raw = 21
    mag = 22
    mag_bias = 23
    mag_wu = 24
    mag_raw_wu = 25
    gra = 28
    gra_wu = 29
    lacc = 31
    lacc_wu = 32
    rv = 34
    rv_wu = 35
    gamerv = 37
    gamerv_wu = 38
    georv = 40
    georv_wu = 41
    ori = 43
    ori_wu = 44
    tilt_detector = 48
    std = 50
    stc = 52
    stc_wu = 53
    sig = 55
    wake_gesture = 57
    glance_gesture = 59
    pickup_gesture = 61
    ar = 63
    wrist_tilt_gesture = 67
    device_ori = 69
    device_ori_wu = 70
    stationary_det = 75
    motion_det = 77
    acc_bias_wu = 91
    gyro_bias_wu = 92
    mag_bias_wu = 93
    std_wu = 94
    ml_1 = 95
    ml_2 = 96
    ml_3 = 97
    air_quality = 115
    head_ori_mis_alg = 120
    imu_head_ori_q = 121
    ndof_head_ori_q = 122
    imu_head_ori_e = 123
    ndof_head_ori_e = 124
    temp = 128
    baro = 129
    hum = 130
    gas = 131
    temp_wu = 132
    baro_wu = 133
    hum_wu = 134
    gas_wu = 135
    stc_lp = 136
    std_lp = 137
    temperature = 138
    stc_lp_wu = 139
    std_lp_wu = 140
    sig_lp_wu = 141
    temperature_wu = 142
    any_motion_lp_wu = 143
    excamera = 144
    gps = 145
    light = 146
    prox = 147
    light_wu = 148
    prox_wu = 149


class BHI360PhysicalSensorId(Enum):
    accelerometer = 1
    not_supported = 2
    gyroscope = 3
    magnetometer = 5
    temp_gyro = 7
    any_motion = 9
    pressure = 11
    position = 13
    humidity = 15
    temperature = 17
    gas_resistor = 19
    phys_step_counter = 32
    phys_step_detector = 33
    phys_sign_motion = 34
    phys_any_motion = 35
    ex_camera_input = 36
    gps = 48
    light = 49
    proximity = 50
    act_rec = 52
    phys_no_motion = 55
    wrist_gesture_detect = 56
    wrist_wear_wakeup = 57


class BHI360ErrorKind(Enum):
    no_error = 0x00
    fw_expected_version_mismatch = 0x10
    fw_bad_header_crc = 0x11
    fw_sha_hash_mismatch = 0x12
    fw_bad_image_crc = 0x13
    fw_ecdsa_signature_verification_failed = 0x14
    fw_bad_public_key_crc = 0x15
    fw_signed_fw_required = 0x16
    fw_header_missing = 0x17
    unexpected_watchdog_reset = 0x19
    rom_version_mismatch = 0x1a
    fatal_firmware_error = 0x1b
    next_payload_not_found = 0x1c
    payload_not_valid = 0x1d
    payload_entries_invalid = 0x1e
    otp_crc_invalid = 0x1f
    firmware_init_failed = 0x20
    unexpected_device_id = 0x21
    no_response_from_device = 0x22
    sensor_init_failed_unknown = 0x23
    sensor_error_no_valid_data = 0x24
    slow_sample_rate = 0x25
    data_overflow = 0x26
    stack_overflow = 0x27
    insufficient_free_ram = 0x28
    driver_parsing_error = 0x29
    ram_banks = 0x2a
    invalid_event = 0x2b
    more_than_32_on_change = 0x2c
    firmware_too_large = 0x2d
    invalid_ram_banks = 0x2f
    math_error = 0x30
    memorry_error = 0x40
    swi3_error = 0x41
    swi4_error = 0x42
    illegal_instruction_error = 0x43
    unhandled_interrupt_exception_postmortem_available = 0x44
    invalid_memory_access = 0x45
    algo_bsx_init = 0x50
    algo_bsx_do_step = 0x51
    algo_update_sub = 0x52
    algo_get_sub = 0x53
    algo_get_phys = 0x54
    algo_unsupported_phys_rate = 0x55
    algo_bsx_driver_not_found = 0x56
    sensor_self_test_failure = 0x60
    sensor_self_test_x_axis_failure = 0x61
    sensor_self_test_y_axis_failure = 0x62
    sensor_self_test_z_axis_failure = 0x64
    sensor_foc_failure = 0x65
    sensor_busy = 0x66
    self_test_foc_unsupported = 0x6f
    no_host_interrupt_set = 0x72
    event_id_size = 0x73
    host_download_channel_underflow = 0x75
    host_upload_channel_overflow = 0x76
    host_download_channel_empty = 0x77
    dma_error = 0x78
    corrupted_input_block_chain = 0x79
    corrupted_output_block_chain = 0x7a
    buffer_block_manager = 0x7b
    input_channel_not_word_aligned = 0x7c
    too_many_flush_events = 0x7d
    unknown_host_channel_error = 0x7e
    decimation_too_large = 0x81
    master_spi_i2c_queue_overflow = 0x90
    spi_i2c_callback_error = 0x91
    timer_scheduling_error = 0xa0
    invalid_gpio_for_host_irq = 0xb0
    sending_initialized_meta_events = 0xb1
    cmd_error = 0xc0
    cmd_too_long = 0xc1
    cmd_buffer_overflow = 0xc2
    sys_call_invalid = 0xd0
    trap_invalid = 0xd2
    fw_header_corrupt = 0xe0
    sensor_data_injection = 0xe2


class Accelerometer:
    scale_2g = 1 / 2 ** 14
    scale_4g = 1 / 2 ** 13
    scale_8g = 1 / 2 ** 12
    scale_16g = 1 / 2 ** 11

    def __init__(self, scale: str) -> None:
        match scale:
            case "2g":
                self.scale = self.scale_8g
            case "4g":
                self.scale = self.scale_4g
            case "8g":
                self.scale = self.scale_8g
            case "16g":
                self.scale = self.scale_16g
            case _:
                self.scale = self.scale_2g

    def convert(self, raw_value: bytes) -> tuple[float,...]:
        x,y,z = struct.unpack(">xhhh", raw_value)
        return x * self.scale, y * self.scale, z * self.scale


class Gyroscope:
    scale_dps_2000 = 1_000 / 2 ** 14
    scale_dps_1000 = 1_000 / 2 ** 15
    scale_dps_500 = 1_000 / 2 ** 16
    scale_dps_250 = 1_000 / 2 ** 17
    scale_dps_125 = 1_000 / 2 ** 18

    def __init__(self, scale: str) -> None:
        match scale:
            case "2000dps":
                self.scale = self.scale_dps_2000
            case "1000dps":
                self.scale = self.scale_dps_1000
            case "500dps":
                self.scale = self.scale_dps_500
            case "250dps":
                self.scale = self.scale_dps_250
            case "125dps":
                self.scale = self.scale_dps_125
            case _:
                self.scale = self.scale_dps_2000

    def convert(self, raw_value: bytes) -> tuple[float,...]:
        x,y,z = struct.unpack(">xhhh", raw_value)
        return x * self.scale, y * self.scale, z * self.scale


class Magnetometer:
    @staticmethod
    def convert(raw_value: bytes) -> tuple[float,...]:
        x,y,z = struct.unpack(">xhhh", raw_value)
        return x, y, z


class QuaternionPlus:
    def __init__(self,) -> None:
        self.scale = 1 / 2 ** 14

    def convert(self, raw_value: bytes) -> tuple[float,...]:
        x,y,z,w, accuracy = struct.unpack(">xhhhhh", raw_value)
        return x * self.scale, y * self.scale, z * self.scale, w * self.scale, accuracy * self.scale


class Quaternion:
    def __init__(self,) -> None:
        self.scale = 1 / 2 ** 14

    def convert(self, raw_value: bytes) -> tuple[float,...]:
        x,y,z,w = struct.unpack(">xhhhh", raw_value)
        return x * self.scale, y * self.scale, z * self.scale, w * self.scale


class Euler:
    def __init__(self,) -> None:
        self.scale = 360 / 2 ** 15

    def convert(self, raw_value: bytes) -> tuple[float,...]:
        heading, pitch, roll = struct.unpack(">xhhh", raw_value)
        return heading * self.scale, pitch * self.scale, roll * self.scale

class Vector3D:
    @staticmethod
    def convert(raw_value: bytes) -> tuple[float,...]:
        x,y,z = struct.unpack(">xhhh", raw_value)
        return x,y,z


class ActivityData:
    @staticmethod
    def convert(raw_value: bytes) -> list[str]:
        activity_bitmap, = struct.unpack(">xH", raw_value)
        still_activity_ended = {"still_activity_ended": activity_bitmap & 0x1}
        walking_activity_ended = {"walking_activity_ended": (activity_bitmap >> 1) & 0x1}
        running_activity_ended = {"running_activity_ended": (activity_bitmap >> 2) & 0x1}
        biking_activity_ended = {"biking_activity_ended": (activity_bitmap >> 3) & 0x1}
        in_vehicle_ended = {"in_vehicle_ended":(activity_bitmap >> 4) & 0x1}
        still_activity_started = {"still_activity_started": (activity_bitmap >> 8) & 0x1}
        walking_activity_started = {"walking_activity_started": (activity_bitmap >> 9) & 0x1}
        running_activity_started = {"running_activity_started": (activity_bitmap >> 10) & 0x1}
        biking_activity_started = {"biking_activity_started": (activity_bitmap >> 11) & 0x1}
        in_vehicle_started = {"in_vehicle_started": (activity_bitmap >> 12) & 0x1}
        activities = {**still_activity_ended,
                      **walking_activity_ended,
                      **running_activity_ended,
                      **biking_activity_ended,
                      **in_vehicle_ended,
                      **still_activity_started,
                      **walking_activity_started,
                      **running_activity_started,
                      **biking_activity_started,
                      **in_vehicle_started,}
        return [key for key in activities if activities[key] == 1]


class MultiTapDetector:
    @staticmethod
    def convert(raw_value: bytes) -> list[str]:
        data, = struct.unpack(">xB", raw_value)
        single_tap = {"single_tap":data & 0x1}
        double_tap = {"double_tap":(data >> 1) & 0x1}
        triple_tap = {"triple_tap":(data >> 2) & 0x1}
        taps = {**single_tap, **double_tap, **triple_tap}
        return [key for key in taps if taps[key] == 1]


class WristGestureDetector:
    @staticmethod
    def convert(raw_value: bytes) -> str:
        data, = struct.unpack(">xB", raw_value)
        if data == 0:
            return "unknown gesture"
        elif data == 3:
            return "wrist shake"
        elif data == 4:
            return "arm flick in gesture"
        elif data == 5:
            return "arm flick out gesture"
        else:
            return "unsupported"



class BHI360:
    def __init__(self) -> None:
        self.read: Callable | None = None
        self.write: Callable | None = None

    def assign_callbacks(self, read_callback: Callable, write_callback: Callable) -> None:
        self.read = read_callback
        self.write = write_callback

    @property
    def chip_id(self) -> int:
        return self.read(BHI360Addr.chip_id)

    @property
    def product_id(self) -> int:
        return self.read(BHI360Addr.product_id)

    @property
    def revision_id(self) -> int:
        return self.read(BHI360Addr.revision_id)

    @property
    def boot_status(self) -> int:
        return self.read(BHI360Addr.boot_status)

    @property
    def describe_boot_status(self) -> str:
        boot_status = self.boot_status
        host_interface_ready = (boot_status >> 4) & 0x01
        firmware_verified = (boot_status >> 5) & 0x01
        firmware_verified_error = (boot_status >> 6) & 0x01
        firmware_halted = (boot_status >> 7) & 0x01
        res = ""
        if host_interface_ready:
            res += "[host interface ready]"
        else:
            res += "[host interface NOT ready]"
        if firmware_verified:
            res += "[firmware verified]"
        if firmware_verified_error:
            res += "[firmware verified ERROR]"
        if firmware_halted:
            res += "[firmware halted]"
        else:
            res += "[firmware running]"
        return res

    @property
    def rom_version(self) -> int:
        val = self.read(BHI360Addr.rom_version_0, 2)
        return val[1] << 8 | val[0]

    @property
    def kernel_version(self) -> int:
        val = self.read(BHI360Addr.kernel_version_0, 2)
        return val[1] << 8 | val[0]

    @property
    def user_version(self) -> int:
        val = self.read(BHI360Addr.user_version_0, 2)
        return val[1] << 8 | val[0]

    @property
    def error_value(self) -> int:
        return self.read(BHI360Addr.error_value)

    @property
    def describe_error_value(self) -> str:
        err = self.error_value
        return BHI360ErrorKind(err).name

    @property
    def host_status(self) -> int:
        return self.read(BHI360Addr.host_status)

    @property
    def describe_host_status(self) -> str:
        host_status = self.host_status
        host_interface_ready = (host_status >> 0) & 0x01
        host_protocol = (host_status >> 1) & 0x01
        host_channel_0_ready = (host_status >> 4) & 0x01
        host_channel_1_ready = (host_status >> 5) & 0x01
        host_channel_2_ready = (host_status >> 6) & 0x01
        host_channel_3_ready = (host_status >> 7) & 0x01
        res = ""
        if host_interface_ready:
            res += "[power state: sleeping]"
        else:
            res += "[power state: active]"
        if host_protocol:
            res += "[protocol: SPI]"
        else:
            res += "[protocol: I2C]"
        if host_channel_0_ready:
            res += "[channel 0 ready]"
        if host_channel_1_ready:
            res += "[channel 1 ready]"
        if host_channel_2_ready:
            res += "[channel 2 ready]"
        if host_channel_3_ready:
            res += "[channel 3 ready]"
        return res

    def request_reset(self) -> None:
        self.write(BHI360Addr.reset_req, 0x01)

    @property
    def host_interface_ctrl(self) -> int:
        return self.read(BHI360Addr.host_interface_ctrl)

    @host_interface_ctrl.setter
    def host_interface_ctrl(self, value: int) -> None:
        self.write(BHI360Addr.host_interface_ctrl, value)
