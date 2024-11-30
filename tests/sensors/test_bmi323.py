import struct
from unittest.mock import patch

from umrx_app_v3.sensors.bmi323 import BMI323


def test_bmi323_read_properties(bmi323: BMI323) -> None:
    all_properties = {key: value for key, value in bmi323.__class__.__dict__.items() if isinstance(value, property)}
    write_only_properties = [
        key for key, value in all_properties.items() if (value.fset is not None) and (value.fget is None)
    ]
    readable_properties = all_properties.keys() - write_only_properties

    for readable_property in readable_properties:
        with patch.object(bmi323, "read") as mocked_read, patch.object(struct, "unpack", return_value=(1, 2, 3)):
            getattr(bmi323, readable_property)
            if readable_property == "sensor_time":
                assert mocked_read.call_count == 2
            else:
                mocked_read.assert_called_once()


def test_bmi323_write_properties(bmi323: BMI323) -> None:
    all_properties = {key: value for key, value in bmi323.__class__.__dict__.items() if isinstance(value, property)}
    writable_properties = [key for key, value in all_properties.items() if value.fset is not None]

    for writable_property in writable_properties:
        with patch.object(bmi323, "write") as mocked_write:
            setattr(bmi323, writable_property, 123)
            mocked_write.assert_called_once()
