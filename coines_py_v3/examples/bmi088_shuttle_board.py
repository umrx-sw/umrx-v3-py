import logging
import sys

from pathlib import Path
from time import sleep

from coines_py_v3.mcu_board.app_board_30 import ApplicationBoard30
from coines_py_v3.shuttle_board.bmi088 import BMI088


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)-8s]:  %(message)s',
        handlers=[
            logging.FileHandler(f'{Path(__file__).stem}.log', mode='w'),
            logging.StreamHandler(sys.stdout),
        ])

    app_board_30 = ApplicationBoard30()
    shuttle = BMI088()

    shuttle.attach_to(app_board_30)

    shuttle.init()
    for _ in range(4):
        shuttle.board.protocol.recv()
    sleep(0.2)
    shuttle.read_gyro_register_spi(0)
    sleep(0.2)
    shuttle.read_accel_register_spi(0)
    sleep(0.2)
    shuttle.read_accel_register_spi(0)
    sleep(0.2)
    shuttle.read_accel_register_spi(2)
    sleep(0.2)
    shuttle.read_accel_register_spi(0x12)
    sleep(0.2)
    shuttle.read_accel_register_spi(0x22)
    sleep(0.2)
    shuttle.read_accel_register_spi(0x23)
    sleep(0.2)
    shuttle.read_accel_register_spi(0x00)
    # shuttle.start_broadcast()
    # sleep(0.1)
    # for packet in shuttle.receive_broadcast(num_packets=1000000):
    #     print(packet)
    #
    # for packet in shuttle.receive_gyro_broadcast(num_packets=1000000):
    #     print(packet)
