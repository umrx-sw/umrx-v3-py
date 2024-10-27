import logging

from umrx_app_v3.mcu_board.bst_app_board import ApplicationBoard

logger = logging.getLogger(__name__)


class AppBoardV3Rev0Error(Exception):
    ...


class ApplicationBoardV3Rev0(ApplicationBoard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, comm='usb')
