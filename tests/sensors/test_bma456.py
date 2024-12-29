from typing import Any
from unittest.mock import patch

from umrx_app_v3.sensors.bma456 import BMA456


def test_bma456_read_properties(bma456: BMA456) -> None:
    def fake_read(*args: Any) -> int | bytes:
        if len(args) <= 1:
            return 42
        return b"b" * args[-1]

    all_properties = {key: value for key, value in bma456.__class__.__dict__.items() if isinstance(value, property)}
    write_only_properties = [
        key for key, value in all_properties.items() if (value.fset is not None) and (value.fget is None)
    ]
    readable_properties = all_properties.keys() - write_only_properties

    for readable_property in readable_properties:
        with patch.object(bma456, "read", side_effect=fake_read) as mocked_read:
            getattr(bma456, readable_property)
            mocked_read.assert_called_once()


def test_bma456_write_properties(bma456: BMA456) -> None:
    all_properties = {key: value for key, value in bma456.__class__.__dict__.items() if isinstance(value, property)}
    writable_properties = [key for key, value in all_properties.items() if value.fset is not None]

    for writable_property in writable_properties:
        with patch.object(bma456, "write") as mocked_write:
            setattr(bma456, writable_property, 123)
            mocked_write.assert_called_once()
