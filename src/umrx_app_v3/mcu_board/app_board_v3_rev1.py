import logging
from typing import Any

from umrx_app_v3.mcu_board.bst_app_board import ApplicationBoard

logger = logging.getLogger(__name__)


class AppBoardV3Rev1Error(Exception): ...


class ApplicationBoardV3Rev1(ApplicationBoard):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, comm="serial")
