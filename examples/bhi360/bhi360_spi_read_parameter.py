import logging
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bhi360.bhi360_shuttle import BHI360Shuttle


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
    shuttle = BHI360Shuttle.on_hardware_v3_rev0()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_spi()
    time.sleep(0.1)
    value = shuttle.sensor.host_interface_ctrl
    logger.info(f"host_interface_ctrl=0x{value:02X}")
    updated_value = value & (~0x80)
    shuttle.sensor.host_interface_ctrl = updated_value
    time.sleep(0.1)
    version = shuttle.firmware_version()
    version = [hex(el) for el in version]
    logger.info(f"got={version}")
