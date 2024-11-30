import struct
from unittest.mock import patch

from umrx_app_v3.sensors.bmi088 import BMI088


def test_bmi088_read_properties(bmi088: BMI088) -> None:
    all_properties = {key: value for key, value in bmi088.__class__.__dict__.items() if isinstance(value, property)}
    write_only_properties = [
        key for key, value in all_properties.items() if (value.fset is not None) and (value.fget is None)
    ]
    readable_properties = all_properties.keys() - write_only_properties

    for readable_property in readable_properties:
        with (
            patch.object(
                bmi088,
                "read_gyro",
                side_effect=lambda *vals: tuple(range(vals[1])) if (isinstance(vals, tuple) and len(vals) > 1) else 1,
            ) as mocked_gyro_read,
            patch.object(
                bmi088,
                "read_accel",
                side_effect=lambda *vals: tuple(range(vals[1])) if (isinstance(vals, tuple) and len(vals) > 1) else 1,
            ) as mocked_acc_read,
            patch.object(struct, "unpack", return_value=(1, 2, 3)),
        ):
            getattr(bmi088, readable_property)
            if readable_property.startswith("gyro_"):
                mocked_gyro_read.assert_called_once()
            elif readable_property.startswith("acc_"):
                mocked_acc_read.assert_called_once()


def test_bmi088_write_properties(bmi088: BMI088) -> None:
    all_properties = {key: value for key, value in bmi088.__class__.__dict__.items() if isinstance(value, property)}
    writable_properties = [key for key, value in all_properties.items() if value.fset is not None]

    for writable_property in writable_properties:
        with (
            patch.object(bmi088, "write_gyro") as mocked_gyro_write,
            patch.object(bmi088, "write_accel") as mocked_accel_write,
        ):
            setattr(bmi088, writable_property, 123)
            if writable_property.startswith("gyro_"):
                mocked_gyro_write.assert_called_once()
            elif writable_property.startswith("acc_"):
                mocked_accel_write.assert_called_once()
