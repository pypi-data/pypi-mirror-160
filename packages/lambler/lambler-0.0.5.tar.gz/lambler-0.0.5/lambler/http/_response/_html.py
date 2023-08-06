from ._http import HttpResponse


class HtmlResponse(HttpResponse):
    def __init__(self, status_code: int, data: str):
        super().__init__(status_code, data, headers={"Content-Type": "text/html; charset=UTF-8"})
