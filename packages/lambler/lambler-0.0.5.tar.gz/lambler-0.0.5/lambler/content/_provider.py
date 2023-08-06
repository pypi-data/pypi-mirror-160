from abc import ABC, abstractmethod
from typing import Any, Optional, Dict


class ContentProvider(ABC):

    @abstractmethod
    def load(self, key: str) -> Any:
        pass


class ContentProviderSpace:
    def __init__(self, mapper: Dict[Optional[str], ContentProvider]):
        self._mapper = mapper

    def get(self, scope: Optional[str]) -> ContentProvider:
        return self._mapper[scope]

    @classmethod
    def from_dict(cls, mapper: Dict[Optional[str], ContentProvider]) -> 'ContentProviderSpace':
        assert isinstance(mapper, dict)
        for key, value in mapper.items():
            assert (isinstance(key, str) or key is None)
            assert isinstance(value, ContentProvider)
        return cls(mapper)

    @classmethod
    def from_provider(cls, provider: ContentProvider) -> 'ContentProviderSpace':
        return cls.from_dict({None: provider})
