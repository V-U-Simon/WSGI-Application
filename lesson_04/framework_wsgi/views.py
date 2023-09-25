from framework_wsgi.http import Response


class View:
    def get(self, request, *args, **kwargs) -> Response:
        pass

    def post(self, request, *args, **kwargs) -> Response:
        pass
