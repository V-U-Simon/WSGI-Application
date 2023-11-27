from typing import Any, Iterable, Type
from .request import Request


class Response:
    def __init__(
        self,
        request: Request,
        status: str = "200 OK",
        body: str = "",
        headers: dict = {},
    ):
        self.request = request
        self.kwargs = {}
        self.status = status

        self.headers = headers
        if hasattr(request, "response_headers"):
            self.headers.update(request.response_headers)
        self.headers_wsgi = {}

        self.body = body.encode("utf-8")

    def headers_to_wsgi(self, base_headers: dict = {}):
        # устанавливаем значение заголовков по умолчанию и
        # обновляем значение заголовков, если обновленные значчения полученные в процессе обработки запроса
        base_headers.update(self.headers)

        # приводим заголовки к определенному wsgi формату
        self.headers_wsgi = [(key, value) for key, value in base_headers.items()]

    def redirect(self, redirect_uri):
        self.status = "302 Found"
        self.headers["Location"] = redirect_uri
        return self
