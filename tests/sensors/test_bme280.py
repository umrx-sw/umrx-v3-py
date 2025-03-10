import struct
from functools import cached_property
from typing import Any
from unittest.mock import patch

from umrx_app_v3.sensors.bme280 import BME280


def test_bme280_read_properties(bme280: BME280) -> None:
    all_properties = {key: value for key, value in bme280.__class__.__dict__.items() if isinstance(value, property)}
    cached_properties = {
        key: value for key, value in bme280.__class__.__dict__.items() if isinstance(value, cached_property)
    }
    write_only_properties = [
        key for key, value in all_properties.items() if (value.fset is not None) and (value.fget is None)
    ]
    readable_properties = (all_properties.keys() - write_only_properties) | cached_properties.keys()

    def fake_read(*args: Any) -> int | bytes:
        if len(args) <= 1:
            return 42
        return b"b" * args[-1]

    for readable_property in readable_properties:
        with (
            patch.object(bme280, "read", side_effect=fake_read) as mocked_read,
            patch.object(struct, "unpack", return_value=(42,)),
        ):
            getattr(bme280, readable_property)
            mocked_read.assert_called_once()

    for readable_property in readable_properties:
        if readable_property.startswith("dig_"):
            with patch.object(bme280, "read", side_effect=fake_read) as mocked_read:
                getattr(bme280, readable_property)
                mocked_read.assert_not_called()


def test_bme280_write_properties(bme280: BME280) -> None:
    all_properties = {key: value for key, value in bme280.__class__.__dict__.items() if isinstance(value, property)}
    writable_properties = [key for key, value in all_properties.items() if value.fset is not None]

    for writable_property in writable_properties:
        with patch.object(bme280, "write") as mocked_write:
            setattr(bme280, writable_property, 123)
            mocked_write.assert_called_once()
