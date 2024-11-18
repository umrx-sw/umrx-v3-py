import logging
import sys
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

    shuttle = BMI088Shuttle.shuttle_on_hardware_v3_rev0()

    shuttle.initialize()
