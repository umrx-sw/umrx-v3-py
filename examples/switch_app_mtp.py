import contextlib

import usb

from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1

if __name__ == "__main__":
    board = ApplicationBoardV3Rev1()
    board.initialize_usb()
    with contextlib.suppress(usb.core.USBError):
        board.switch_usb_mtp()
