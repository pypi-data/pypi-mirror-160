class Param:
    def __init__(self, key: str):
        self._key = key

    @property
    def key(self) -> str:
        return self._key
