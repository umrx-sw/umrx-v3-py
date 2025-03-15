import logging
import sys
import time
from pathlib import Path

from umrx_app_v3.shuttle_board.bmm350.bmm350_shuttle import BMM350Shuttle


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
    shuttle = BMM350Shuttle.on_hardware_v3_rev1()
    shuttle.initialize()
    shuttle.check_connected_hw()

    shuttle.configure_i2c()

    logger.info(f"chip_id=0x{shuttle.sensor.chip_id:02X}")
    logger.info(f"err_reg=0x{shuttle.sensor.err_reg:02X}")
    logger.info(f"pmu_cmd_aggr_set=0x{shuttle.sensor.pmu_cmd_aggr_set:02X}")
    logger.info(f"pmu_cmd_axis_en=0x{shuttle.sensor.pmu_cmd_axis_en:02X}")

    logger.info(f"magnetometer_raw={shuttle.sensor.magnetometer_raw}")
    logger.info(f"temperature_raw={shuttle.sensor.temperature_raw:08X}")
    _ = shuttle.sensor.compensate_magnetometer_and_temperature(0, 0, 0, 0)  # cache OTP
    shuttle.close_otp()
    shuttle.start_measurement()
    time.sleep(0.1)
    logger.info(f"pmu_cmd_status_0=0b{shuttle.sensor.pmu_cmd_status_0:08b}")
    logger.info(f"pmu_cmd_status_1=0b{shuttle.sensor.pmu_cmd_status_1:08b}")

    magnetometer_raw = shuttle.sensor.magnetometer_raw
    temperature_raw = shuttle.sensor.temperature_raw
    m_x, m_y, m_z, temp = shuttle.sensor.compensate_magnetometer_and_temperature(*magnetometer_raw, temperature_raw)
    logger.info(f"magnetometer(uT)=(x={m_x}, y={m_y}, z={m_z})")
    logger.info(f"temperature(C)={temp}")
    logger.info(f"sensor_time(s)={shuttle.sensor.sensor_time}")
