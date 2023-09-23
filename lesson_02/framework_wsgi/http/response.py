from typing import Any, Iterable
from framework_wsgi.middleware import middleware


class Response:
    def __init__(self, status: str, headers: Iterable, body: Any):
        print(f"Processing response")
        self.status = status
        self.headers = headers
        self.body = body

        for func in middleware.post_process_funcs:
            func(self)
