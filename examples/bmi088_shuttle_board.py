import logging
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bmi088.bmi088_shuttle import BMI088Shuttle

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)-8s]:  %(message)s",
        handlers=[
            logging.FileHandler(f"{Path(__file__).stem}.log", mode="w"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    shuttle = BMI088Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_i2c()
    logging.info(f"acc_chip_id=0x{shuttle.sensor.acc_chip_id:02X}")
    logging.info(f"gyro_chip_id=0x{shuttle.sensor.gyro_chip_id:02X}")

    time.sleep(0.1)
    shuttle.configure_spi()
    _ = shuttle.board.read_spi(shuttle.CSB1, 0, 1)  # first read is required

    logging.info(f"acc_chip_id=0x{shuttle.sensor.acc_chip_id:02X}")
    logging.info(f"gyro_chip_id=0x{shuttle.sensor.gyro_chip_id:02X}")

    time.sleep(0.1)
    logging.info(f"acc_status=0x{shuttle.sensor.acc_status:02X}")
    logging.info(f"acc_fifo_config_1=0x{shuttle.sensor.acc_fifo_config_1:02X}")

    logging.info(f"acc_conf=0x{shuttle.sensor.acc_conf:02X}")
