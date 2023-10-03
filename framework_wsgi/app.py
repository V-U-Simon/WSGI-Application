from pprint import pprint
import re
from typing import Callable, Iterable, Type
from framework_wsgi.debug_decorator import debug

from framework_wsgi.urls import Url
from framework_wsgi.views import View, page_not_found
from framework_wsgi.http import Request, Response
from framework_wsgi.middleware import BaseMiddleWare
from framework_wsgi.exceptions import MethodNotAllowed, PageNotFound


class Application:
    def __init__(
        self,
        urls: list[Type[Url]],
        middlewares: list[Type[BaseMiddleWare],],
        settings: dict,
    ) -> None:
        self.urls = urls
        self.middlewares = middlewares
        self.settings = settings

    def __call__(self, environ: dict, start_response) -> Iterable:
        request = self._get_request(environ)
        response = self._get_response(request)

        # отправляем заголовки, статус и возвращаем итерируемый объект (т.к. тело может быть слишком большим)
        start_response(response.status, response.headers_wsgi)
        return [response.body]

    def _get_request(self, environ: dict):
        request = Request(environ)
        request.settings = self.settings

        for middleware in self.middlewares:
            middleware.process_request(request)
        return request

    def _get_response(self, request) -> Response:
        view: View | Callable = self._find_view(request)
        view_method = self._get_method_if_view_class(view, request)
        response: Response = view_method(request, **request.kwargs)

        for middleware in self.middlewares:
            middleware.process_response(response)

        response.headers_to_wsgi(base_headers=self.settings.DEFAULT_HEADERS)
        return response

    def _find_view(self, request) -> Callable:
        try:
            for path in self.urls:
                matched_params = path.match(request.url)
                if matched_params is not None:
                    request.kwargs = matched_params  # Извлечение параметров из URL
                    return path.view
            raise PageNotFound
        except PageNotFound:
            return page_not_found

    def _get_method_if_view_class(self, view: View, request) -> Callable:
        # if issubclass(view, View):
        # проверка: view является классом
        if isinstance(view, type):
            method = request.method.lower()
            if not hasattr(view, method):
                raise MethodNotAllowed
            return getattr(view(), method)
        else:
            return view


class FakeApplication(Application):
    def __call__(self, environ, start_response):
        start_response("200 OK", [("Content-Type", "text/html")])
        return [b"200 OK"]


class DebugApplication(Application):
    """Отладочное приложение, выводит время подготовки ответа в консоль"""

    def __init__(
        self,
        urls: list[type[Url]],
        middlewares: list[type[BaseMiddleWare]],
        settings: dict,
    ) -> None:
        print("DEBUG MODE")
        super().__init__(urls, middlewares, settings)

    def __call__(self, environ: dict, start_response) -> Iterable:
        return super().__call__(environ, start_response)

    @debug
    def _get_response(self, request) -> Response:
        return super()._get_response(request)
