import logging
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
    # For using with Application board 3.0, replace the line below with:
    # shuttle = BMI088Shuttle.on_hardware_v3_rev0()
    shuttle = BMI088Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_i2c()
    logger.info(f"acc_chip_id=0x{shuttle.sensor.acc_chip_id:02X}")
    logger.info(f"gyro_chip_id=0x{shuttle.sensor.gyro_chip_id:02X}")

    logger.info(f"acc_status=0x{shuttle.sensor.acc_status:02X}")
    logger.info(f"acc_fifo_config_1=0x{shuttle.sensor.acc_fifo_config_1:02X}")

    logger.info(f"acc_conf=0x{shuttle.sensor.acc_conf:02X}")
    shuttle.switch_on_accel()
    time.sleep(0.1)
    logger.info(f"acceleration={shuttle.sensor.acceleration}")
    logger.info(f"gyro={shuttle.sensor.gyro_rate}")
