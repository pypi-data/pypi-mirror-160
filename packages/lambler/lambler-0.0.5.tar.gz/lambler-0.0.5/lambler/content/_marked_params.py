from typing import Dict

from ._content import Content
from ._provider import ContentProviderSpace


def build_marked_params(content_providers: ContentProviderSpace, marker: Content) -> Dict:
    return content_providers.get(marker.scope).load(marker.key)
