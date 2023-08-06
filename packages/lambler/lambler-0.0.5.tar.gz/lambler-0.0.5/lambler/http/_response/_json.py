from typing import Dict

from ._http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, status_code: int, data: Dict):
        super().__init__(status_code, data, headers={"Content-Type": "application/json"})
