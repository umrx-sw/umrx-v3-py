import logging
import struct
from functools import cached_property
from typing import Any
from unittest.mock import patch

import pytest

from umrx_app_v3.sensors.bmm350 import BMM350, BMM350Error, BMM350OtpAddr

logger = logging.getLogger(__name__)


def test_bmm350_read_properties(bmm350: BMM350) -> None:
    all_properties = {key: value for key, value in bmm350.__class__.__dict__.items() if isinstance(value, property)}
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
            patch.object(bmm350, "read", side_effect=fake_read) as mocked_read,
            patch.object(struct, "unpack", return_value=(42,)),
        ):
            getattr(bmm350, readable_property)
            mocked_read.assert_called_once()


def test_bmm350_write_properties(bmm350: BMM350) -> None:
    all_properties = {key: value for key, value in bmm350.__class__.__dict__.items() if isinstance(value, property)}
    writable_properties = [key for key, value in all_properties.items() if value.fset is not None]

    for writable_property in writable_properties:
        with patch.object(bmm350, "write") as mocked_write:
            setattr(bmm350, writable_property, 123)
            mocked_write.assert_called_once()


def test_bmm350_otp_properties(bmm350: BMM350) -> None:
    cached_properties = {
        key: value for key, value in bmm350.__class__.__dict__.items() if isinstance(value, cached_property)
    }

    def fake_read(*args: Any) -> int | bytes:
        if len(args) <= 1:
            return 0
        return b"b" * args[-1]

    def fake_write(*args: Any) -> int | bytes:
        pass

    for cached_read in cached_properties:
        if cached_read.startswith("otp_"):
            with (
                patch.object(bmm350, "read", side_effect=fake_read) as mocked_read,
                patch.object(bmm350, "write", side_effect=fake_write) as mocked_write,
            ):
                getattr(bmm350, cached_read)
                assert mocked_read.call_count == 3
                mocked_write.assert_called_once()


def test_signed_8_bit(bmm350: BMM350) -> None:
    assert bmm350.sign_convert_8_bit(0) == 0
    assert bmm350.sign_convert_8_bit(127) == 127
    assert bmm350.sign_convert_8_bit(128) == -128
    assert bmm350.sign_convert_8_bit(255) == -1


def test_signed_12_bit(bmm350: BMM350) -> None:
    assert bmm350.sign_convert_12_bit(0) == 0
    assert bmm350.sign_convert_12_bit(2047) == 2047
    assert bmm350.sign_convert_12_bit(2048) == -2048
    assert bmm350.sign_convert_12_bit(4095) == -1


def test_signed_16_bit(bmm350: BMM350) -> None:
    assert bmm350.sign_convert_16_bit(0) == 0
    assert bmm350.sign_convert_16_bit(32767) == 32767
    assert bmm350.sign_convert_16_bit(32768) == -32768
    assert bmm350.sign_convert_16_bit(65535) == -1


def test_signed_24_bit(bmm350: BMM350) -> None:
    assert bmm350.sign_convert_24_bit(0) == 0
    assert bmm350.sign_convert_24_bit(8_388_607) == 8_388_607
    assert bmm350.sign_convert_24_bit(8_388_608) == -8_388_608
    assert bmm350.sign_convert_24_bit(16_777_215) == -1


def test_assign_callbacks(bmm350: BMM350) -> None:
    read_callback = lambda: 42  # noqa: E731
    write_callback = lambda *values: None  # noqa: E731, ARG005
    bmm350.assign_callbacks(read_callback, write_callback)
    assert bmm350.read == read_callback
    assert bmm350.write == write_callback


def test_incorrect_opt_status_raises(bmm350: BMM350) -> None:
    def fake_read(*args: Any) -> int:
        return 0xFF

    def fake_write(*args: Any) -> int | bytes: ...

    with (
        patch.object(bmm350, "read", side_effect=fake_read),
        patch.object(bmm350, "write", side_effect=fake_write),
        pytest.raises(BMM350Error),
    ):
        bmm350.read_otp_word(BMM350OtpAddr.cross_x_y)
