import logging
import struct
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bmi323.bmi323_shuttle import BMI323Shuttle


def setup_logging(level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(level)
    stdout_handler = logging.StreamHandler(sys.stdout)
    log_format = "(%(asctime)s) [%(levelname)-8s] %(filename)s:%(lineno)d:  %(message)s"
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
    shuttle = BMI323Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_i2c()
    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:04X}")
    assert shuttle.sensor.chip_id == 0x0043
    shuttle.configure_polling_streaming()
    shuttle.start_streaming()
    time.sleep(0.1)
    for idx in range(1000):
        for streaming in shuttle.board.receive_polling_streaming_multiple():
            sensor_id, payload = streaming
            a_x, a_y, a_z, g_x, g_y, g_z, temperature, time_stamp = struct.unpack("<xxhhhhhhHI", payload)
            temperature_c = 23 + (temperature / 512)
            time_stamp_second = time_stamp * 39.0625 / 1e6
            logger.info(
                f"[{idx=}], accel({a_x=:+05d}, {a_y=:+05d}, {a_z=:+05d}), gyro({g_x=:+05d}, {g_y=:+05d}, {g_z=:+05d}), "
                f"T={temperature_c:+2.3f}, time_stamp(sec)={time_stamp_second:.6f}"
            )
        time.sleep(0.05)
    shuttle.board.stop_polling_streaming()
