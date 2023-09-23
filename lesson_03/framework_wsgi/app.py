from typing import Iterable

from . import front_controller
from .http import Request, Response
from .middleware import middleware


class Application:
    def __init__(self) -> None:
        self.middleware = middleware

    def __call__(self, environ: dict, start_response) -> Iterable:
        request = Request(environ)
        view = front_controller.get_page(request.path)
        status, body = view(request)
        response = Response(status, body)

        # отправляем заголовки, статус и возвращаем итерируемый объект (т.к. тело может быть слишком большим)
        start_response(response.status, response.headers)
        return [response.body]
