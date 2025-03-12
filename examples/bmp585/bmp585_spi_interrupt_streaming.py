import logging
import struct
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
    assert shuttle.sensor.chip_id == 0x51
    shuttle.configure_interrupt_streaming()
    shuttle.start_streaming()
    time.sleep(0.1)
    for idx in range(1000):
        for streaming in shuttle.board.receive_interrupt_streaming_multiple(includes_mcu_timestamp=False):
            sensor_id, packet, time_stamp, payload = streaming
            (temp_xlsb, temp_lsb, temp_msb, pressure_xlsb, pressure_lsb, pressure_msb) = struct.unpack(
                "<BBBBBB", payload
            )
            pressure = ((pressure_msb << 16) | (pressure_lsb << 8) | pressure_xlsb) / 2**6
            (full_degrees,) = struct.unpack("<b", int.to_bytes(temp_msb, 1, byteorder="little"))
            fractional_degrees = ((temp_lsb << 8) | temp_xlsb) / 2**16
            temperature = full_degrees + fractional_degrees
            logger.info(f"[{idx=:03d}], pressure(Pa)={pressure:7.3f}, temperature(C)={temperature:3.3f}")
        time.sleep(0.05)
    shuttle.board.stop_interrupt_streaming()
