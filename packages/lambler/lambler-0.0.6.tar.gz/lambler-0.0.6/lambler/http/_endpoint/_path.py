import re
from typing import Dict, List


class EndpointPath:
    def __init__(self, pattern: re.Pattern, keys: List[str]):
        self._pattern = pattern
        self._keys = keys

    @classmethod
    def create(cls, path: str) -> 'EndpointPath':
        keys = re.findall(r"\{(.*?)}", path)
        pattern_str = '^' + re.sub(r"\{.*?}", r"(.*?)", path) + '/?$'
        pattern = re.compile(pattern_str)
        return cls(pattern, keys)

    def match(self, path: str) -> (int, bool):
        matched = self._pattern.match(path)
        if matched is None:
            return 0, False

        start, end = matched.span()
        length = end - start + 1
        return length, True

    def extract_params(self, path: str) -> Dict[str, str]:
        params = self._pattern.findall(path)
        return {key: params[i] for i, key in enumerate(self._keys)}
