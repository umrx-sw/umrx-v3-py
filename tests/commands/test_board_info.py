import pytest
from array import array

from umrx_app_v3.mcu_board.commands.board_info import BoardInfoCmd, BoardInfo

@pytest.mark.app_board
def test_app_board_parse_board_info(board_info_cmd: BoardInfoCmd) -> None:
    resp = array("B", [0xAA, 0x0F, 0x01, 0x00, 0x42, 0x1F, 0x01, 0x41, 0x00, 0x10, 0x00, 0x09, 0x05, 0x0D, 0x0A])
    board_info = board_info_cmd.parse(resp)

    assert isinstance(board_info, BoardInfo)

    assert board_info.hardware_id == 0x10

    assert board_info.software_id == 0x09

    assert board_info.board_id == 0x05

    assert board_info.shuttle_id == 0x141
