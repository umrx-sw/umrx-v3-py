import abc
import inspect
import logging
from array import array
from collections.abc import Callable
from typing import Any, Optional

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
        packet_start = 0xAA
        is_packet_start_found = packet[0] == packet_start
        packet_size = packet[1]
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
