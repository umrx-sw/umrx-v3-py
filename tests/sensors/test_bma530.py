from typing import Any
from unittest.mock import patch

from umrx_app_v3.sensors.bma530 import BMA530, BMA530ExtendedAddr


def test_bma530_read_properties(bma530: BMA530) -> None:
    def fake_read(*args: Any) -> int | bytes:
        if len(args) <= 1:
            return 42
        return b"b" * args[-1]

    def fake_write(*args: Any) -> None: ...

    all_properties = {key: value for key, value in bma530.__class__.__dict__.items() if isinstance(value, property)}
    write_only_properties = [
        key for key, value in all_properties.items() if (value.fset is not None) and (value.fget is None)
    ]
    readable_properties = all_properties.keys() - write_only_properties

    for readable_property in readable_properties:
        with (
            patch.object(bma530, "read", side_effect=fake_read) as mocked_read,
            patch.object(bma530, "write", side_effect=fake_write),
        ):
            getattr(bma530, readable_property)
            mocked_read.assert_called_once()


def test_bma580_write_properties(bma530: BMA530) -> None:
    all_properties = {key: value for key, value in bma530.__class__.__dict__.items() if isinstance(value, property)}
    writable_properties = [key for key, value in all_properties.items() if value.fset is not None]

    extended_register_names = set(BMA530ExtendedAddr.__members__.keys())
    main_register_map_exceptions = {"acc_offset_x", "acc_offset_y", "acc_offset_z"}
    for writable_property in writable_properties:
        with patch.object(bma530, "write") as mocked_write:
            setattr(bma530, writable_property, 123)
            if writable_property in extended_register_names | main_register_map_exceptions:
                assert mocked_write.call_count == 2
            else:
                mocked_write.assert_called_once()
