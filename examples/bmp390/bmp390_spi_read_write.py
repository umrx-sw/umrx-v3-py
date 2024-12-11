import logging
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bmp390.bmp390_shuttle import BMP390Shuttle


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
    shuttle = BMP390Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_spi()
    _ = shuttle.board.read_spi(shuttle.CS, 0, 1)  # dummy read is required, do not delete

    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:02X}")
    logger.info(f"rev_id=0x{shuttle.sensor.rev_id:02X}")
    logger.info(f"err_reg=0x{shuttle.sensor.err_reg:02X}")
    logger.info(f"status=0x{shuttle.sensor.status:02X}")
    logger.info(f"pwr_ctrl=0b{shuttle.sensor.pwr_ctrl:08b}")
    logger.info(f"odr=0b{shuttle.sensor.odr:08b}")
    logger.info(f"osr=0b{shuttle.sensor.osr:08b}")

    shuttle.sensor.pwr_ctrl = (1 << 0) | (1 << 1) | (0b11 << 4)
    time.sleep(0.1)
    logger.info(f"pwr_ctrl=0b{shuttle.sensor.pwr_ctrl:08b}")

    raw_temperature = shuttle.sensor.temperature
    compensated_temperature = shuttle.sensor.compensate_temperature(raw_temperature)
    logger.info(f"temperature(raw)=0x{raw_temperature:06X}, temperature(C)={compensated_temperature}")
    raw_pressure = shuttle.sensor.pressure
    compensated_pressure = shuttle.sensor.compensate_pressure(raw_pressure, compensated_temperature)
    logger.info(f"pressure(raw)=0x{raw_pressure:06X}, pressure(Pa)={compensated_pressure}")
    logger.info(f"sensor_time=0x{shuttle.sensor.sensor_time:06X}")
