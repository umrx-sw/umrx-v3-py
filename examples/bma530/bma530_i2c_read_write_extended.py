import contextlib
import logging
import sys
import time
from pathlib import Path

from umrx_app_v3.mcu_board.commands.command import CommandError
from umrx_app_v3.shuttle_board.bma530.bma530_shuttle import BMA530Shuttle


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
    shuttle = BMA530Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_i2c()
    with contextlib.suppress(CommandError):
        dummy = shuttle.read_register(0, 1)
    time.sleep(0.1)

    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:02X}")
    shuttle.switch_on_accel()
    shuttle.sensor.int2_conf = 0x01
    time.sleep(0.1)
    logger.info(f"feat_conf_err={shuttle.sensor.feat_conf_err}")

    logger.info(f"step_counter=0x{shuttle.sensor.step_counter:04X}")
    logger.info(f"tilt_1=0x{shuttle.sensor.tilt_1:04X}")
    logger.info(f"tilt_2=0x{shuttle.sensor.tilt_2:04X}")

    logger.info(f"generic_interrupt1_1=0x{shuttle.sensor.generic_interrupt1_1:04X}")

    shuttle.sensor.generic_interrupt1_1 = 0xABCD
    time.sleep(0.05)
    logger.info(f"generic_interrupt1_1=0x{shuttle.sensor.generic_interrupt1_1:04X}")

    assert shuttle.sensor.generic_interrupt1_1 == 0xABCD
