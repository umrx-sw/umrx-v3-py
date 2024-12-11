import struct
from typing import Any
from unittest.mock import patch

from umrx_app_v3.sensors.bmp390 import BMP390

# def test_bmp390_cached_properties(bmp390: BMP390) -> None:
#     all_properties = {key: value for key, value in bmp390.__class__.__dict__.items() if isinstance(value, property)}
#     write_only_properties = [
#         key for key, value in all_properties.items() if (value.fset is not None) and (value.fget is None)
#     ]
#     readable_properties = all_properties.keys() - write_only_properties
#
#     for readable_property in readable_properties:
#         with patch.object(bmp390, "read") as mocked_read, patch.object(struct, "unpack", return_value=(1, 2, 3)):
#             getattr(bmp390, readable_property)
#             if readable_property == "sensor_time":
#                 assert mocked_read.call_count == 2
#             else:
#                 mocked_read.assert_called_once()


def test_bmp390_read_properties(bmp390: BMP390) -> None:
    all_properties = {key: value for key, value in bmp390.__class__.__dict__.items() if isinstance(value, property)}
    write_only_properties = [
        key for key, value in all_properties.items() if (value.fset is not None) and (value.fget is None)
    ]
    readable_properties = all_properties.keys() - write_only_properties

    def fake_read(*args: Any) -> int | bytes:
        if len(args) <= 1:
            return 42
        return b"b" * args[-1]

    for readable_property in readable_properties:
        with (
            patch.object(bmp390, "read", side_effect=fake_read) as mocked_read,
            patch.object(struct, "unpack", return_value=(42,)),
        ):
            if not readable_property.startswith("par_"):
                getattr(bmp390, readable_property)
                mocked_read.assert_called_once()

    for readable_property in readable_properties:
        if readable_property.startswith("par_"):
            with patch.object(bmp390, "read", side_effect=fake_read) as mocked_read:
                getattr(bmp390, readable_property)
                mocked_read.assert_not_called()


def test_bmp390_write_properties(bmp390: BMP390) -> None:
    all_properties = {key: value for key, value in bmp390.__class__.__dict__.items() if isinstance(value, property)}
    writable_properties = [key for key, value in all_properties.items() if value.fset is not None]

    for writable_property in writable_properties:
        with patch.object(bmp390, "write") as mocked_write:
            setattr(bmp390, writable_property, 123)
            mocked_write.assert_called_once()
