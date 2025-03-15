import logging
import struct
import sys
import time
from pathlib import Path

from umrx_app_v3.sensors.bmm350 import BMM350
from umrx_app_v3.shuttle_board.bmm350.bmm350_shuttle import BMM350Shuttle


def setup_logging(level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(level)
    stdout_handler = logging.StreamHandler(sys.stdout)
    log_format = "(%(asctime)s) [%(levelname)-8s] %(message)s"
    log_formatter = logging.Formatter(log_format)
    stdout_handler.setFormatter(log_formatter)
    file_handler = logging.FileHandler(f"{Path(__file__).parent / Path(__file__).stem}.log", mode="w")
    file_handler.setFormatter(log_formatter)
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)
    return logger


if __name__ == "__main__":
    logger = setup_logging()
    # This example is for Application Board 3.1 hardware
    shuttle = BMM350Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_i2c()
    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:04X}")
    assert shuttle.sensor.chip_id == 0x33
    _ = shuttle.sensor.compensate_magnetometer_and_temperature(0, 0, 0, 0)  # cache OTP
    shuttle.close_otp()
    shuttle.configure_polling_streaming()
    shuttle.start_streaming()
    time.sleep(0.1)
    for idx in range(1000):
        for streaming in shuttle.board.receive_polling_streaming_multiple():
            sensor_id, payload = streaming
            (
                m_x_xlsb,
                m_x_lsb,
                m_x_msb,
                m_y_xlsb,
                m_y_lsb,
                m_y_msb,
                m_z_xlsb,
                m_z_lsb,
                m_z_msb,
                temp_xlsb,
                temp_lsb,
                temp_msb,
                time_xlsb,
                time_lsb,
                time_msb,
            ) = struct.unpack("<xxBBBBBBBBBBBBBBB", payload)
            m_x_raw = (m_x_msb << 16) | (m_x_lsb << 8) | m_x_xlsb
            m_y_raw = (m_y_msb << 16) | (m_y_lsb << 8) | m_y_xlsb
            m_z_raw = (m_z_msb << 16) | (m_z_lsb << 8) | m_z_xlsb
            m_x_signed, m_y_signed, m_z_signed = BMM350.sign_convert_magnetometer(m_x_raw, m_y_raw, m_z_raw)
            temp_raw = (temp_msb << 16) | (temp_lsb << 8) | temp_xlsb
            temp_signed = BMM350.sign_convert_24_bit(temp_raw)
            sensor_time = ((time_msb << 16) | (time_lsb << 8) | time_xlsb) * 39.0625e-6
            m_x, m_y, m_z, temp = shuttle.sensor.compensate_magnetometer_and_temperature(
                m_x_signed, m_y_signed, m_z_signed, temp_signed
            )
            logger.info(
                f"[{idx=:03d}], magnetometer(uT)=(x={m_x:+3.3f}, y={m_y:+3.3f}, z={m_z:+3.3f}), "
                f"temperature(C)={temp:.3f}, "
                f"time_stamp(s)={sensor_time:.3f}"
            )
        time.sleep(0.05)
    shuttle.board.stop_polling_streaming()
