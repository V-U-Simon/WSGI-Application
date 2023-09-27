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
        self.status = status

        self.headers = headers
        self.headers_wsgi = {}

        self.body = body.encode("utf-8")

    def headers_to_wsgi(self, base_headers: dict = {}):
        base_headers.update(self.headers)
        self.headers_wsgi = [(key, value) for key, value in base_headers.items()]
