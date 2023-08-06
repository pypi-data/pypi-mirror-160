from typing import Any

from ._provider import ContentProvider


class LocalFile(ContentProvider):
    def load(self, key: str) -> Any:
        with open(key) as file:
            return file.read()
