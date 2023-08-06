import inspect
from typing import Any

from lambler.http._event import HttpEvent


class Header:
    def __init__(self, key: str):
        self._key = key

    def __repr__(self) -> str:
        return f"Header({self._key!r})"

    @staticmethod
    def validate_param(param: inspect.Parameter) -> None:
        type_ = param.annotation

        if not issubclass(type_, str):
            raise TypeError("Header marker can only be used with type 'str'")

    def extract_event(self, event: HttpEvent) -> Any:
        return event.headers[self._key]
