import logging
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
    shuttle = BMI323Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_i2c()

    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:04X}")
    logger.info(f"err_reg=0x{shuttle.sensor.err_reg:04X}")
    logger.info(f"status=0x{shuttle.sensor.status:04X}")

    a_x, a_y, a_z = shuttle.sensor.acc_data
    logger.info(f"acceleration=({a_x=:04X}, {a_y=:04X}, {a_z=:04X})")

    g_x, g_y, g_z = shuttle.sensor.gyr_data
    logger.info(f"angular_velocity=({g_x=:04X}, {g_y=:04X}, {g_z=:04X})")

    logger.info(f"sensor_time={shuttle.sensor.sensor_time:04X}")

    logger.info(f"acc_conf=0x{shuttle.sensor.acc_conf:04X}")
    logger.info(f"gyr_conf=0x{shuttle.sensor.gyr_conf:04X}")

    shuttle.sensor.acc_conf = 0x4027
    shuttle.sensor.gyr_conf = 0x404B

    logger.info(f"acc_conf=0x{shuttle.sensor.acc_conf:04X}")
    logger.info(f"gyr_conf=0x{shuttle.sensor.gyr_conf:04X}")

    logger.info(f"alt_acc_conf=0x{shuttle.sensor.alt_acc_conf:04X}")
    logger.info(f"alt_gyr_conf=0x{shuttle.sensor.alt_gyr_conf:04X}")
    time.sleep(0.1)
    a_x, a_y, a_z = shuttle.sensor.acc_data
    logger.info(f"acceleration=({a_x=}, {a_y=}, {a_z=})")

    g_x, g_y, g_z = shuttle.sensor.gyr_data
    logger.info(f"angular_velocity=({g_x=}, {g_y=}, {g_z=})")
