import logging
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bma400.bma400_shuttle import BMA400Shuttle


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
    shuttle = BMA400Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_i2c()

    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:02X}")
    logger.info(f"err_reg=0x{shuttle.sensor.err_reg:02X}")
    logger.info(f"status=0x{shuttle.sensor.status:02X}")

    logger.info(f"acceleration={shuttle.sensor.acc_data}")
    logger.info(f"sensor_time={shuttle.sensor.sensor_time}")
    shuttle.switch_on_accel()
    time.sleep(0.1)
    logger.info(f"acceleration={shuttle.sensor.acc_data}")
    logger.info(f"sensor_time={shuttle.sensor.sensor_time}")
