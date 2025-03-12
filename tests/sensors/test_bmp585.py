import logging
import struct
from typing import Any
from unittest.mock import patch

from umrx_app_v3.sensors.bmp585 import BMP585

logger = logging.getLogger(__name__)


def test_bmp390_read_properties(bmp585: BMP585) -> None:
    all_properties = {key: value for key, value in bmp585.__class__.__dict__.items() if isinstance(value, property)}

    def fake_read(*args: Any) -> int | bytes:
        if len(args) <= 1:
            return 42
        return b"b" * args[-1]

    for readable_property in all_properties:
        with (
            patch.object(bmp585, "read", side_effect=fake_read) as mocked_read,
            patch.object(struct, "unpack", return_value=(42,)),
        ):
            getattr(bmp585, readable_property)
            mocked_read.assert_called_once()


def test_bmp390_write_properties(bmp585: BMP585) -> None:
    all_properties = {key: value for key, value in bmp585.__class__.__dict__.items() if isinstance(value, property)}
    writable_properties = [key for key, value in all_properties.items() if value.fset is not None]

    for writable_property in writable_properties:
        with patch.object(bmp585, "write") as mocked_write:
            setattr(bmp585, writable_property, 123)
            mocked_write.assert_called_once()
