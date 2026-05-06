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

    shuttle.configure_i2c()

    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:02X}")
    logger.info(f"fuser2_product_id=0x{shuttle.sensor.product_id:02X}")
    logger.info(f"fuser2_revision_id=0x{shuttle.sensor.revision_id:02X}")
    logger.info(f"boot_status={shuttle.sensor.describe_boot_status}")
    current_folder = Path(__file__).parent
    firmware_file = current_folder / "firmware" / "Bosch_Shuttle3_BHI360.fw"
    shuttle.upload_firmware_to_ram(firmware_file)
    time.sleep(0.5)
    shuttle.boot_program_ram()
    time.sleep(0.5)
    logger.info(f"kernel_version={shuttle.sensor.kernel_version}")
    logger.info(f"user_version={shuttle.sensor.user_version}")
    logger.info(f"rom_version={shuttle.sensor.rom_version}")
    logger.info(f"boot_status={shuttle.sensor.describe_boot_status}")
    logger.info(f"error_value={shuttle.sensor.describe_error_value}")
