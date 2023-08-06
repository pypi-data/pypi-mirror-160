from typing import Callable, Any, TypeVar, Dict, List

from lambler.base import Handler
from ._endpoint import Endpoint
from ._response import HttpResponse
from ..content import ContentProviderSpace

T = TypeVar("T", bound=Callable)


class HttpApi(Handler):
    def __init__(self):
        self._endpoints: List[Endpoint] = []

    def get(self, path: str) -> Callable[[Callable], Any]:
        def decorator(f: T) -> T:
            self._endpoints.append(Endpoint.create(path, f))
            return f

        return decorator

    def set_content_provider_space(self, providers: ContentProviderSpace):
        for endpoint in self._endpoints:
            endpoint.set_content_provider_space(providers)

    def handle(self, event: Dict, context: Any):
        longest_path_length = 0
        longest_path_executor = None

        for endpoint in self._endpoints:
            executor = endpoint.match(event, context)
            if executor is not None and executor.path_length > longest_path_length:
                longest_path_length = executor.path_length
                longest_path_executor = executor

        if longest_path_executor is not None:
            response = longest_path_executor.execute()
            if response is not None:
                assert isinstance(response, HttpResponse)
                return response.to_dict()
            return http_response(200, "")


def http_response(status_code: int, body: str) -> Dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "text/plain",
        },
        "body": body,
        "cookies": [],
        "isBase64Encoded": False
    }
