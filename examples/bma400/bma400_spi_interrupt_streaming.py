import logging
import struct
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bma400.bma400_shuttle import BMA400Shuttle


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
    shuttle = BMA400Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_spi()
    _ = shuttle.board.read_spi(shuttle.CS, 0, 1)  # dummy read is required, do not delete

    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:02X}")
    assert shuttle.sensor.chip_id == 0x90
    shuttle.configure_interrupt_streaming()
    shuttle.start_streaming()
    time.sleep(0.1)
    for idx in range(1000):
        for streaming in shuttle.board.receive_interrupt_streaming_multiple(includes_mcu_timestamp=False):
            sensor_id, packet, time_stamp, payload = streaming
            a_x, a_y, a_z, t_0, t_1, t_2 = struct.unpack("<xHHHBBB", payload)
            a_x, a_y, a_z = shuttle.sensor.sign_convert_accel(a_x, a_y, a_z)
            sensor_time = ((t_2 << 16) | (t_1 << 8) | t_0) * 39.0625e-6
            logger.info(
                f"[{idx=:03d}], acceleration(a_x={a_x:+5d}, a_y={a_y:+5d}, a_z={a_z:+5d}), "
                f"time_stamp(s)={sensor_time:.3f}"
            )
        time.sleep(0.05)
    shuttle.board.stop_interrupt_streaming()