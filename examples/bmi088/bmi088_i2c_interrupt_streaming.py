import logging
import struct
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bmi088.bmi088_shuttle import BMI088Shuttle


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
    shuttle = BMI088Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_i2c()
    logger.info(f"acc_chip_id=0x{shuttle.sensor.acc_chip_id:02X}")
    logger.info(f"gyro_chip_id=0x{shuttle.sensor.gyro_chip_id:02X}")
    assert shuttle.sensor.acc_chip_id == 0x1E
    assert shuttle.sensor.gyro_chip_id == 0x0F
    shuttle.configure_interrupt_streaming()
    shuttle.start_streaming()
    time.sleep(0.1)
    for idx in range(1000):
        for streaming in shuttle.board.receive_interrupt_streaming_multiple(includes_mcu_timestamp=False):
            sensor_id, packet, time_stamp, payload = streaming
            d_x, d_y, d_z = struct.unpack("<hhh", payload)
            if sensor_id == 1:
                logger.info(f"[{idx}][a] {packet=:06d} a_x={d_x:04d}, a_y={d_y:04d}, a_z={d_z:04d}")
            elif sensor_id == 2:
                logger.info(f"[{idx}][g] {packet=:06d} g_x={d_x:04d}, g_y={d_y:04d}, g_z={d_z:04d}")
        time.sleep(0.05)
    shuttle.board.stop_interrupt_streaming()
