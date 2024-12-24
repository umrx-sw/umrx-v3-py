import struct
from unittest.mock import patch

from umrx_app_v3.sensors.bma400 import BMA400


def test_bma400_read_properties(bma400: BMA400) -> None:
    all_properties = {key: value for key, value in bma400.__class__.__dict__.items() if isinstance(value, property)}
    write_only_properties = [
        key for key, value in all_properties.items() if (value.fset is not None) and (value.fget is None)
    ]
    readable_properties = all_properties.keys() - write_only_properties

    for readable_property in readable_properties:
        with (
            patch.object(bma400, "read", return_value=(1, 2, 3)) as mocked_read,
            patch.object(struct, "unpack", return_value=(1, 2, 3)),
        ):
            getattr(bma400, readable_property)
            mocked_read.assert_called_once()


def test_bma400_write_properties(bma400: BMA400) -> None:
    all_properties = {key: value for key, value in bma400.__class__.__dict__.items() if isinstance(value, property)}
    writable_properties = [key for key, value in all_properties.items() if value.fset is not None]

    for writable_property in writable_properties:
        with patch.object(bma400, "write") as mocked_write:
            setattr(bma400, writable_property, 123)
            mocked_write.assert_called_once()
