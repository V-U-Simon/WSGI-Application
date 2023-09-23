from typing import Any, Iterable
from framework_wsgi.middleware import middleware


HEADERS: Iterable = [
    ("Content-Type", "text/html; charset=UTF-8"),
    # ("Content-Type", "application/json"),
]


class Response:
    def __init__(self, status: str, body: Any, headers: Iterable = HEADERS):
        print(f"Processing response")
        self.body = body
        self.status = status
        self.headers = headers = headers

        for func in middleware.post_process_funcs:
            func(self)
