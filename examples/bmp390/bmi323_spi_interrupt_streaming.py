import logging
import struct
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bmi323.bmi323_shuttle import BMI323Shuttle


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
    shuttle = BMI323Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_spi()
    _ = shuttle.board.read_spi(shuttle.CS, 0, 1)  # dummy read is required, do not delete

    logger.info(f"acc_chip_id=0x{shuttle.sensor.chip_id:04X}")
    assert shuttle.sensor.chip_id == 0x0043
    shuttle.configure_interrupt_streaming()
    shuttle.start_streaming()
    time.sleep(0.1)
    for idx in range(1000):
        for streaming in shuttle.board.receive_interrupt_streaming_multiple(includes_mcu_timestamp=False):
            sensor_id, packet, time_stamp, payload = streaming
            if sensor_id == 1:
                a_x, a_y, a_z = struct.unpack("<xhhh", payload)
                logger.info(f"[{idx}][{packet}][a] {' ' * 30} a_x={a_x:04d}, a_y={a_y:04d}, a_z={a_z:04d} ")
            elif sensor_id == 2:
                g_x, g_y, g_z = struct.unpack("<xhhh", payload)
                logger.info(f"[{idx}][{packet}][g] g_x={g_x:04d}, g_y={g_y:04d}, g_z={g_z:04d} ")
        time.sleep(0.05)
    shuttle.board.stop_interrupt_streaming()
