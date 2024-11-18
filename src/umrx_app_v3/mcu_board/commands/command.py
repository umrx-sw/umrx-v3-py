import abc
import inspect
import logging
from array import array
from collections.abc import Callable
from typing import Any, Optional

from umrx_app_v3.mcu_board.bst_protocol_constants import (
    CoinesResponse,
    CommandId,
    ErrorCode,
)

logger = logging.getLogger(__name__)


class CommandError(Exception): ...


class Command(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def assemble(*args: Optional, **kwargs: Optional) -> Any: ...

    @staticmethod
    @abc.abstractmethod
    def parse(message: array[int]) -> Any: ...

    @staticmethod
    def create_message_from(payload: array[int] | tuple[int, ...] | list[int]) -> array:
        message_start_length = 1 + 1  # start byte 0xAA and message length byte
        message_end_length = 1 + 1  # stop bytes 0xD 0xA (CR LF)
        message_length = message_start_length + len(payload) + message_end_length
        message = array("B", message_length * [255])
        message[0] = 0xAA
        message[1] = message_length
        message[2:-2] = array("B", payload)
        message[-2], message[-1] = 0xD, 0xA
        return message

    @staticmethod
    def check_message(packet: array[int] | tuple[int, ...] | list[int]) -> bool:
        if len(packet) < 2:
            return False
        packet_start = 0xAA
        is_packet_start_found = packet[0] == packet_start
        packet_size = packet[1]
        if len(packet) < packet_size:
            return False
        packet_end = 0x0D, 0x0A
        is_packet_end_found = tuple(packet[packet_size - 2 : packet_size]) == packet_end
        return is_packet_start_found and is_packet_end_found

    @staticmethod
    def check_message_length(*, expected: int = 0, not_less_then: int = 0) -> Callable:
        def decorator(function: Callable) -> Callable:
            def wrapper(*args: Any, **kwargs: Any) -> None | Any:
                message = kwargs["message"] if kwargs.get("message") else args[0]
                wrapper.__signature__ = inspect.signature(function)
                if expected and len(message) != expected:
                    logger.error("Expected message length: %s got %s", expected, len(message))
                    logger.error("Check failed, function `%s` will not be executed ", function.__name__)
                    return None
                if not_less_then and len(message) < not_less_then:
                    logger.error("Expect message of length at least %s: got %s", not_less_then, len(message))
                    logger.error("Check failed, function `%s` will not be executed ", function.__name__)
                    return None
                return function(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def parse_read_response(message: array[int]) -> array[int]:
        if not Command.check_message(message):
            error_message = f"Cannot parse invalid message {message}"
            raise CommandError(error_message)
        message_len = message[1]
        message_feature = message[CoinesResponse.DD_RESPONSE_FEATURE_POSITION.value]
        feature_correct = message_feature == CommandId.SENSOR_WRITE_AND_READ.value
        message_status = message[CoinesResponse.DD_RESPONSE_STATUS_POSITION.value]
        status_ok = message_status == ErrorCode.SUCCESS.value
        if not (feature_correct and status_ok):
            error_message = f"Error in message: {feature_correct=}, {status_ok=}, {message_status=}, {message=}"
            raise CommandError(error_message)

        extended_read_idx = CoinesResponse.DD_RESPONSE_COMMAND_ID_POSITION.value
        if message[extended_read_idx] == CoinesResponse.DD_RESPONSE_EXTENDED_READ_ID.value:
            payload_msb = message[CoinesResponse.DD_RESPONSE_PACKET_LENGTH_MSB_POSITION.value]
            payload_lsb = message[CoinesResponse.DD_RESPONSE_PACKET_LENGTH_LSB_POSITION.value]
            payload_len = (payload_msb << 8) | payload_lsb
        else:
            payload_len = message_len - CoinesResponse.DD_RESPONSE_OVERHEAD_BYTES.value

        payload_start = CoinesResponse.DD_RESPONSE_OVERHEAD_BYTES.value - 2
        return array("B", (int(el) for el in message[payload_start : payload_start + payload_len]))

    @staticmethod
    def check_for_max_payload(data_to_write: array[int]) -> tuple[bool, str]:
        max_payload_size = 46
        if len(data_to_write) > max_payload_size:
            error_message = f"Cannot write > {max_payload_size} at once, attempted {len(data_to_write)}. Split payload"
            return False, error_message
        return True, ""
