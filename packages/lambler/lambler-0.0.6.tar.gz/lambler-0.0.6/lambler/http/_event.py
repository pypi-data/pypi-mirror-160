from typing import Dict, Any


class HttpEvent:
    def __init__(self, path: str, headers: Dict[str, Any], query_params: Dict[str, str]):
        self.path = path
        self.headers = headers
        self.query_params = query_params

    @classmethod
    def from_dict(cls, raw: Dict) -> 'HttpEvent':
        return cls(raw["rawPath"], raw["headers"], raw.get("queryStringParameters", {}))
