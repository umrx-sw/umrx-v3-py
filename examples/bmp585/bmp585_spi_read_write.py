import logging
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bmp585.bmp585_shuttle import BMP585Shuttle


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
    shuttle = BMP585Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_spi()
    _ = shuttle.board.read_spi(shuttle.CS, 0, 1)  # dummy read is required, do not delete

    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:02X}")
    logger.info(f"rev_id=0x{shuttle.sensor.rev_id:02X}")
    logger.info(f"chip_status=0x{shuttle.sensor.chip_status:02X}")
    logger.info(f"status=0x{shuttle.sensor.status:02X}")
    logger.info(f"drive_config=0b{shuttle.sensor.drive_config:08b}")
    logger.info(f"int_config=0b{shuttle.sensor.int_config:08b}")
    logger.info(f"dsp_config=0b{shuttle.sensor.dsp_config:08b}")
    logger.info(f"odr_config=0b{shuttle.sensor.odr_config:08b}")
    shuttle.sensor.osr_config = 1 << 6
    shuttle.sensor.odr_config = (1 << 7) | (0x0 << 2) | (0b11 << 0)
    time.sleep(0.1)
    logger.info(f"odr_config=0b{shuttle.sensor.odr_config:08b}")
    logger.info(f"osr_config=0b{shuttle.sensor.osr_config:08b}")

    temperature = shuttle.sensor.temperature
    logger.info(f"temperature(C)={temperature}")
    pressure = shuttle.sensor.pressure
    logger.info(f"pressure(Pa)={pressure}")
