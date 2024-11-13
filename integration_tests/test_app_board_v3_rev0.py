import logging
import struct
import time
from array import array

import pytest

from umrx_app_v3.mcu_board.app_board_v3_rev0 import ApplicationBoardV3Rev0
from umrx_app_v3.mcu_board.bst_app_board import BoardInfo
from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, PinDirection, PinValue, StreamingSamplingUnit

logger = logging.getLogger(__name__)


@pytest.mark.app_board
def test_app_board_v3_rev0_board_info(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.protocol.communication.connect()
    info = app_board_v3_rev0.board_info
    assert isinstance(info, BoardInfo), "Expecting BoardInfo instance"
    assert info.board_id == 0x05, "Wrong board ID"
    assert info.hardware_id == 0x10, "Wrong hardware ID"
    assert info.software_id == 0x09, "Wrong software ID"
    # assert info.shuttle_id == 0x66, "Wrong shuttle ID for BMI08x"
    assert info.shuttle_id == 0x141, "Wrong shuttle ID for BMI08x"


def test_app_board_v3_rev0_switch_app_mtp(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.protocol.communication.connect()
    app_board_v3_rev0.switch_usb_mtp()


def test_app_board_v3_rev0_switch_app_dfu(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.protocol.communication.connect()
    app_board_v3_rev0.switch_usb_dfu_bl()


def test_app_board_v3_rev0_read_bmi088_i2c_accel(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.initialize()
    app_board_v3_rev0.start_communication()
    info = app_board_v3_rev0.board_info
    assert info.shuttle_id == 0x66, "The integration test works only with BMI088"
    app_board_v3_rev0.set_vdd_vddio(3.3, 3.3)
    time.sleep(0.5)
    app_board_v3_rev0.configure_i2c()
    resp = app_board_v3_rev0.read_i2c(0x18, 0x0, 1)
    assert resp[0] == 0x1E, "Expect correct address for BMI088 accelerometer"


def test_gyro(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.initialize()
    app_board_v3_rev0.start_communication()
    info = app_board_v3_rev0.board_info
    assert info.shuttle_id == 0x66, "The integration test works only with BMI088"
    app_board_v3_rev0.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6, PinDirection.OUTPUT, PinValue.HIGH)
    app_board_v3_rev0.set_vdd_vddio(3.3, 3.3)
    time.sleep(0.5)
    app_board_v3_rev0.configure_i2c()
    resp = app_board_v3_rev0.read_i2c(0x68, 0x0, 1)
    assert resp[0] == 0x0F, "Expect correct address for BMI088 gyroscope"


def test_app_board_v3_rev0_spi_read_write(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.initialize()
    app_board_v3_rev0.start_communication()
    info = app_board_v3_rev0.board_info
    assert info.shuttle_id == 0x66, "The integration test works only with BMI088"
    app_board_v3_rev0.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_1, PinDirection.OUTPUT, PinValue.HIGH)
    app_board_v3_rev0.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_5, PinDirection.OUTPUT, PinValue.HIGH)
    app_board_v3_rev0.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6, PinDirection.OUTPUT, PinValue.LOW)
    time.sleep(0.01)
    app_board_v3_rev0.set_vdd_vddio(3.3, 3.3)
    time.sleep(0.2)
    app_board_v3_rev0.configure_spi()
    time.sleep(0.2)
    resp = app_board_v3_rev0.read_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_1, 0x0, 1)
    logger.info("Initial read from accel, otherwise subsequent reads do not work")

    resp = app_board_v3_rev0.read_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_5, 0x0, 1)
    logger.info(f"chip-id gyro: {resp}, hex=0x{resp[0]:0X}")
    assert resp[0] == 0x0F, "Expect correct address for BMI088 gyroscope"

    resp = app_board_v3_rev0.read_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_1, 0x0, 2)
    logger.info(f"chip-id accel: {resp}, hex=0x{resp[0]:0X}")
    assert resp[1] == 0x1E, "Expect correct address for BMI088 accelerometer"

    app_board_v3_rev0.write_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_1, 0x7C, array("B", (0x00,)))
    app_board_v3_rev0.write_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_1, 0x7D, array("B", (0x04,)))
    time.sleep(0.2)
    resp = app_board_v3_rev0.read_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_1, 0x7C, 3)
    pwr_save_mode, acc_enable = resp[1], resp[2]
    logger.info(f"accel mode: {pwr_save_mode=}, {acc_enable=}")
    assert pwr_save_mode == 0x00
    assert acc_enable == 0x04

    accel = app_board_v3_rev0.read_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_1, 0x12, 10)
    accel.append(0)
    _, a_x, a_y, a_z, time_stamp = struct.unpack("<chhhI", accel)
    logger.info(f"accel data: {accel}")
    time_stamp_seconds = time_stamp / (100 * 2**8)
    logger.info(f"{a_x=}, {a_y=}, {a_z=}, {time_stamp=}, {time_stamp_seconds=}")

    gyro = app_board_v3_rev0.read_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_5, 0x02, 6)
    g_x, g_y, g_z = struct.unpack("<hhh", gyro)
    logger.info(f"gyro data: {gyro}")
    logger.info(f"{g_x=}, {g_y=}, {g_z=}")


def test_streaming_polling_i2c_accel_and_gyro(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.initialize()
    app_board_v3_rev0.start_communication()
    info = app_board_v3_rev0.board_info
    assert info.shuttle_id == 0x66, "The integration test works only with BMI088"
    app_board_v3_rev0.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6, PinDirection.OUTPUT, PinValue.HIGH)
    app_board_v3_rev0.set_vdd_vddio(3.3, 3.3)
    app_board_v3_rev0.configure_i2c()
    # power on accelerometer - it is OFF by default
    app_board_v3_rev0.write_i2c(0x18, 0x7C, array("B", (0x00, 0x04)))
    app_board_v3_rev0.streaming_polling_set_i2c_channel(
        i2c_address=0x18,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=6,
    )
    app_board_v3_rev0.streaming_polling_set_i2c_channel(
        i2c_address=0x68,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )
    app_board_v3_rev0.configure_streaming_polling(interface="i2c")

    app_board_v3_rev0.start_streaming()
    logger.info("start streaming")
    time.sleep(0.5)
    for _ in range(100):
        streaming = app_board_v3_rev0.receive_streaming()
        sensor_id, payload = streaming
        data_x, data_y, data_z = struct.unpack("<hhh", payload)
        if sensor_id == 1:
            logger.info(f"[a] a_x={data_x:04d}, a_y={data_y:04d}, a_z={data_z:04d} ")
        elif sensor_id == 2:
            logger.info(f"[g] g_x={data_x:04d}, g_y={data_y:04d}, g_z={data_z:04d} ")
        time.sleep(0.05)
    app_board_v3_rev0.stop_polling_streaming()


def test_streaming_polling_spi_accel_and_gyro(app_board_v3_rev0: ApplicationBoardV3Rev0) -> None:
    app_board_v3_rev0.initialize()
    app_board_v3_rev0.start_communication()
    info = app_board_v3_rev0.board_info
    assert info.shuttle_id == 0x66, "The integration test works only with BMI088"
    app_board_v3_rev0.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_1, PinDirection.OUTPUT, PinValue.HIGH)
    app_board_v3_rev0.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_5, PinDirection.OUTPUT, PinValue.HIGH)
    app_board_v3_rev0.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6, PinDirection.OUTPUT, PinValue.LOW)
    app_board_v3_rev0.set_vdd_vddio(3.3, 3.3)
    app_board_v3_rev0.configure_spi()

    resp = app_board_v3_rev0.read_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_5, 0x0, 1)
    logger.info(f"chip-id gyro: {resp}")
    # assert resp[0] == 0x0F, "Expect correct address for BMI088 gyroscope"

    resp = app_board_v3_rev0.read_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_1, 0x0, 1)
    # assert resp[0] == 0x1E, "Expect correct address for BMI088 accelerometer"
    logger.info(f"chip-id accel: {resp}")
    # time.sleep(0.1)
    # # power on accelerometer - it is OFF by default
    app_board_v3_rev0.write_spi(MultiIOPin.MINI_SHUTTLE_PIN_2_1, 0x7C, array("B", (0x00, 0x00, 0x04)))
    app_board_v3_rev0.streaming_polling_set_spi_channel(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_1,
        sampling_time=625,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x12,
        bytes_to_read=6,
    )
    app_board_v3_rev0.streaming_polling_set_spi_channel(
        cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5,
        sampling_time=500,
        sampling_unit=StreamingSamplingUnit.MICRO_SECOND,
        register_address=0x02,
        bytes_to_read=6,
    )
    app_board_v3_rev0.configure_streaming_polling(interface="spi")

    app_board_v3_rev0.start_streaming()
    logger.info("start streaming")
    time.sleep(0.5)
    for _ in range(100):
        streaming = app_board_v3_rev0.receive_streaming()
        sensor_id, payload = streaming
        data_x, data_y, data_z = struct.unpack("<hhh", payload)
        if sensor_id == 1:
            logger.info(f"[a] a_x={data_x:04d}, a_y={data_y:04d}, a_z={data_z:04d} ")
        elif sensor_id == 2:
            logger.info(f"[g] g_x={data_x:04d}, g_y={data_y:04d}, g_z={data_z:04d} ")
        time.sleep(0.05)
    app_board_v3_rev0.stop_polling_streaming()
