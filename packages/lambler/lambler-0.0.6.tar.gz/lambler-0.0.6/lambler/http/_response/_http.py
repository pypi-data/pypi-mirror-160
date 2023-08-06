from typing import Any, Dict


class HttpResponse:
    def __init__(self, status_code: int, body: Any, *, headers: Dict[str, str] = None):
        self._status_code = status_code
        self._body = body
        self._headers = headers or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "statusCode": self._status_code,
            "headers": self._headers,
            "body": self._body,
            "cookies": [],
            "isBase64Encoded": False,
        }
