class Content:
    def __init__(self, key: str, *, scope: str = None):
        self._key = key
        self._scope = scope

    @property
    def key(self) -> str:
        return self._key

    @property
    def scope(self) -> str:
        return self._scope
