import logging
import struct
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bme280.bme280_shuttle import BME280Shuttle


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
    shuttle = BME280Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_spi()
    _ = shuttle.board.read_spi(shuttle.CS, 0, 1)  # dummy read is required, do not delete

    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:02X}")
    assert shuttle.sensor.chip_id == 0x60
    _ = shuttle.sensor.compensate_temperature(0x0000)  # caching NVM registers
    _ = shuttle.sensor.compensate_pressure(0x00, 0x00)  # caching NVM registers
    _ = shuttle.sensor.compensate_humidity(0x00, 0x00)  # caching NVM registers
    shuttle.configure_polling_streaming()
    shuttle.start_streaming()
    time.sleep(0.1)
    for idx in range(1000):
        for streaming in shuttle.board.receive_polling_streaming_multiple():
            sensor_id, payload = streaming
            (pressure_msb, pressure_lsb, pressure_xlsb, temp_msb, temp_lsb, temp_xlsb, hum_msb, hum_lsb) = (
                struct.unpack("<BBBBBBBB", payload)
            )
            raw_pressure = (pressure_msb << 12) | (pressure_lsb << 4) | ((pressure_xlsb >> 4) & 0x0F)
            raw_temperature = (temp_msb << 12) | (temp_lsb << 4) | ((temp_xlsb >> 4) & 0x0F)
            raw_humidity = (hum_msb << 8) | hum_lsb
            compensated_temperature = shuttle.sensor.compensate_temperature(raw_temperature)
            compensated_pressure = shuttle.sensor.compensate_pressure(raw_pressure, raw_temperature)
            compensated_humidity = shuttle.sensor.compensate_humidity(raw_humidity, raw_temperature)
            logger.info(
                f"[{idx=:03d}], pressure(Pa)={compensated_pressure:7.3f}, "
                f"temperature(C)={compensated_temperature:3.3f}, "
                f"humidity(%RH)={compensated_humidity:3.3f}"
            )
        time.sleep(0.05)
    shuttle.board.stop_polling_streaming()
