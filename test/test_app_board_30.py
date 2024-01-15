#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 29 May 2022

import logging
from typing import List, Tuple, Union

import pytest

from array import array
from coines_py_v3.mcu_board.bst_protocol import BstProtocol
from coines_py_v3.mcu_board.usb_comm import UsbCommunication
from coines_py_v3.mcu_board.app_board_30 import ApplicationBoard30, BoardInfo

logger = logging.getLogger()


@pytest.mark.app_board
def test_app_board_30_construction(app_board_30: ApplicationBoard30):
    assert isinstance(app_board_30, ApplicationBoard30), "Expecting instance of ApplicationBoard30"
    assert isinstance(app_board_30.protocol, BstProtocol), "Expecting BST protocol object inside App Board 3.0"


@pytest.mark.app_board
def test_app_board_30_board_info(app_board_30: ApplicationBoard30):
    info = app_board_30.board_info
    assert isinstance(info, BoardInfo), "Expecting BoardInfo instance"
    assert info.board_id == 0x05, "Wrong board ID"
    assert info.hardware_id == 0x10, "Wrong hardware ID"
    assert info.software_id == 0x09, "Wrong software ID"
    assert info.shuttle_id == 0x66, "Wrong shuttle ID for BMI08x"
