import abc
from typing import Any


class Communication(abc.ABC):
    @abc.abstractmethod
    def send(self, message: Any) -> bool: ...

    @abc.abstractmethod
    def receive(self) -> Any: ...

    @abc.abstractmethod
    def send_receive(self, message: Any) -> Any: ...

    @abc.abstractmethod
    def find_device(self) -> None: ...

    @abc.abstractmethod
    def initialize(self) -> None: ...

    @abc.abstractmethod
    def connect(self) -> None: ...

    @abc.abstractmethod
    def disconnect(self) -> None: ...
