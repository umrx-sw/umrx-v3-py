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
    shuttle.configure_polling_streaming()
    shuttle.start_streaming()
    time.sleep(0.1)
    for idx in range(1000):
        for streaming in shuttle.board.receive_polling_streaming_multiple():
            sensor_id, payload = streaming
            data_x, data_y, data_z = struct.unpack("<hhh", payload)
            if sensor_id == 1:
                logger.info(f"[{idx}][a] a_x={data_x:04d}, a_y={data_y:04d}, a_z={data_z:04d} ")
            elif sensor_id == 2:
                logger.info(f"[{idx}][g] g_x={data_x:04d}, g_y={data_y:04d}, g_z={data_z:04d} ")
        time.sleep(0.05)
    shuttle.board.stop_polling_streaming()
