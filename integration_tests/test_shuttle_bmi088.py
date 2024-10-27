import logging
import struct
from array import array

import pytest

from umrx_app_v3.mcu_board.app_board_v3_rev0 import ApplicationBoardV3Rev0
from umrx_app_v3.shuttle_board.bmi088 import BMI088

logger = logging.getLogger()


@pytest.mark.bmi08x
def test_bmi088_construction(bmi088: BMI088, caplog):
    assert isinstance(bmi088, BMI088), "Expecting instance of BMI088"
    assert isinstance(bmi088.board, ApplicationBoardV3Rev0), f"Expecting ApplicationBoard30, got {type(bmi088.board)}"


@pytest.mark.bmi08x
def test_bmi088_check_gyro_broadcast(bmi088: BMI088):
    valid_packet = 170, 18, 1, 0, 135, 244, 255, 176, 255, 54, 0, 0, 0, 0, 0, 2, 13, 10
    packet = array("B", valid_packet)
    should_be_valid = bmi088.is_gyro_broadcast(packet)
    assert should_be_valid, "Check if valid gyro packet identified"

    wrong_length_packet = 170, 26, 1, 0, 135, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 1, 128, 0, 0, 16, 0, 0, 0, 1, 13, 10
    packet = array("B", wrong_length_packet)
    should_be_invalid = bmi088.is_gyro_broadcast(packet)
    assert not should_be_invalid, "Check if invalid gyro packet NOT identified"


@pytest.mark.bmi08x
def test_bmi088_check_accel_broadcast(bmi088: BMI088):
    valid_broadcast_packet = 170, 26, 1, 0, 135, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 1, 128, 0, 0, 16, 0, 0, 0, 1, 13, 10
    packet = array("B", valid_broadcast_packet)
    should_be_valid = bmi088.is_accel_broadcast(packet)
    assert should_be_valid, "Check if valid accel packet identified"

    wrong_length_packet = 170, 18, 1, 0, 135, 244, 255, 176, 255, 54, 0, 0, 0, 0, 0, 2, 13, 10
    packet = array("B", wrong_length_packet)
    should_be_invalid = bmi088.is_accel_broadcast(packet)
    assert not should_be_invalid, "Check if invalid accel packet NOT identified"


@pytest.mark.bmi08x
def test_bmi088_gyro_broadcast_decode(bmi088: BMI088):
    valid_packet = 170, 18, 1, 0, 135, 244, 255, 176, 255, 54, 0, 0, 0, 0, 0, 2, 13, 10
    packet = array("B", valid_packet)
    decoded_gyro_packet = bmi088.decode(packet)

    g_x_raw_unsigned = (packet[6] << 8) | packet[5]
    expected_g_x_raw, *_ = struct.unpack(">h", struct.pack(">H", g_x_raw_unsigned))
    assert decoded_gyro_packet.g_x_raw == expected_g_x_raw, "Raw value g_x_raw is wrong!"

    g_y_raw_unsigned = (packet[8] << 8) | packet[7]
    expected_g_y_raw, *_ = struct.unpack(">h", struct.pack(">H", g_y_raw_unsigned))
    assert decoded_gyro_packet.g_y_raw == expected_g_y_raw, "Raw value g_y_raw is wrong!"

    g_z_raw_unsigned = (packet[10] << 8) | packet[9]
    expected_g_z_raw, *_ = struct.unpack(">h", struct.pack(">H", g_z_raw_unsigned))
    assert decoded_gyro_packet.g_z_raw == expected_g_z_raw, "Raw value g_z_raw is wrong!"

    raw_unpack = struct.unpack("<HHH", packet[5:11])
    assert raw_unpack[0] == g_x_raw_unsigned, "Interpretation of the g_x_raw is wrong"
    assert raw_unpack[1] == g_y_raw_unsigned, "Interpretation of the g_y_raw is wrong"
    assert raw_unpack[2] == g_z_raw_unsigned, "Interpretation of the g_z_raw is wrong"


@pytest.mark.bmi08x
def test_bmi088_accel_broadcast_decode(bmi088: BMI088):

    valid_packet = 170, 26, 1, 0, 135, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 1, 128, 0, 0, 16, 0, 0, 0, 1, 13, 10
    packet = array("B", valid_packet)
    decoded_accel_packet = bmi088.decode(packet)

    a_x_raw_unsigned = (packet[7] << 8) | packet[6]
    expected_a_x_raw, *_ = struct.unpack(">h", struct.pack(">H", a_x_raw_unsigned))
    assert decoded_accel_packet.a_x_raw == expected_a_x_raw, "Raw value a_x_raw is wrong!"

    a_y_raw_unsigned = (packet[9] << 8) | packet[8]
    expected_a_y_raw, *_ = struct.unpack(">h", struct.pack(">H", a_y_raw_unsigned))
    assert decoded_accel_packet.a_y_raw == expected_a_y_raw, "Raw value a_y_raw is wrong!"

    a_z_raw_unsigned = (packet[11] << 8) | packet[10]
    expected_a_z_raw, *_ = struct.unpack(">h", struct.pack(">H", a_z_raw_unsigned))
    assert decoded_accel_packet.a_z_raw == expected_a_z_raw, "Raw value a_z_raw is wrong!"

    raw_unpack = struct.unpack("<HHH", packet[6:12])
    assert raw_unpack[0] == a_x_raw_unsigned, "Interpretation of the a_x_raw is wrong"
    assert raw_unpack[1] == a_y_raw_unsigned, "Interpretation of the a_y_raw is wrong"
    assert raw_unpack[2] == a_z_raw_unsigned, "Interpretation of the a_z_raw is wrong"
