import logging
import struct
import sys
import time
from pathlib import Path

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

    shuttle.configure_spi()
    _ = shuttle.board.read_spi(shuttle.CS, 0, 1)  # dummy read is required, do not delete

    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:02X}")
    assert shuttle.sensor.chip_id == 0xC2
    shuttle.configure_polling_streaming()
    shuttle.start_streaming()
    time.sleep(0.1)
    for idx in range(1000):
        for streaming in shuttle.board.receive_polling_streaming_multiple():
            sensor_id, payload = streaming
            a_x, a_y, a_z, temp, t_0, t_1, t_2 = struct.unpack("<xhhhBBBB", payload)
            sensor_time = ((t_2 << 16) | (t_1 << 8) | t_0) * 312.5e-6
            logger.info(
                f"[{idx=:03d}], acceleration(a_x={a_x:4d}, a_y={a_y:4d}, a_z={a_z:4d}), "
                f"time_stamp(s)={sensor_time:.3f}"
            )
        time.sleep(0.05)
    shuttle.board.stop_polling_streaming()
