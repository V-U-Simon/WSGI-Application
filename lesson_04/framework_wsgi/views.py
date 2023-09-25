from framework_wsgi.http import Response
from framework_wsgi.templator import render


class View:
    def get(self, request, *args, **kwargs) -> Response:
        pass

    def post(self, request, *args, **kwargs) -> Response:
        pass


def page_not_found(request) -> Response:
    response = render(request, "page_not_found.html")
    response.status = "404 Not Found"
    return response
