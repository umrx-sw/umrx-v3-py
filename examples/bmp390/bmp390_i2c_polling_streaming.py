import logging
import struct
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
    # This example is for Application Board 3.1 hardware
    shuttle = BMP390Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_i2c()
    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:04X}")
    assert shuttle.sensor.chip_id == 0x60
    _ = shuttle.sensor.compensate_temperature(0x0000)  # caching NVM registers
    _ = shuttle.sensor.compensate_pressure(0x00, 24.0)  # caching NVM registers
    shuttle.configure_polling_streaming()
    shuttle.start_streaming()
    time.sleep(0.1)
    for idx in range(1000):
        for streaming in shuttle.board.receive_polling_streaming_multiple():
            sensor_id, payload = streaming
            (pressure_b0, pressure_b1, pressure_b2, temp_b0, temp_b1, temp_b2, time_b0, time_b1, time_b2) = (
                struct.unpack("<BBBBBBxxBBB", payload)
            )
            raw_pressure = (pressure_b2 << 16) | (pressure_b1 << 8) | pressure_b0
            raw_temperature = (temp_b2 << 16) | (temp_b1 << 8) | temp_b0
            sensor_time = (time_b2 << 16) | (time_b1 << 8) | time_b0
            compensated_temperature = shuttle.sensor.compensate_temperature(raw_temperature)
            compensated_pressure = shuttle.sensor.compensate_pressure(raw_pressure, compensated_temperature)
            logger.info(
                f"[{idx=:03d}], pressure(Pa)={compensated_pressure:7.3f}, "
                f"temperature(C)={compensated_temperature:3.3f}, "
                f"time_stamp(s)={sensor_time / 25908.533}"
            )
        time.sleep(0.05)
    shuttle.board.stop_polling_streaming()
