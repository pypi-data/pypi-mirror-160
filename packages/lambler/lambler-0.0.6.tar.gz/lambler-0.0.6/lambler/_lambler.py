from typing import Dict, Any, List, Union, Optional

from .base import Handler
from .content import ContentProvider, ContentProviderSpace

ContentProviderAllowedType = Union[ContentProvider, Dict[Optional[str], ContentProvider]]


class Lambler:
    def __init__(self):
        self._handlers: List[Handler] = []
        self._content_providers: Optional[ContentProviderSpace] = None

    def handle(self, *handlers: Handler):
        self._handlers = handlers

        self._ensure_handler_with_content_provider()

    def __call__(self, event: Dict, context: Any):
        return self._handlers[0].handle(event, context)

    def use_content(self, provider: ContentProviderAllowedType):
        self._content_providers = _make_content_provider_space(provider)

        self._ensure_handler_with_content_provider()

    def _ensure_handler_with_content_provider(self):
        if self._content_providers is None:
            return

        for handler in self._handlers:
            handler.set_content_provider_space(self._content_providers)


def _make_content_provider_space(provider: ContentProviderAllowedType) -> ContentProviderSpace:
    if isinstance(provider, dict):
        return ContentProviderSpace.from_dict(provider)
    elif isinstance(provider, ContentProvider):
        return ContentProviderSpace.from_provider(provider)
    raise NotImplementedError()
