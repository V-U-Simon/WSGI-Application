from typing import Type

from urllib.parse import parse_qs
import cgi


class Request:
    def __init__(self, environ: dict):
        self.url = self._prepare_url(environ["PATH_INFO"])
        self.environ = environ
        self.method = environ["REQUEST_METHOD"].upper()
        self.cookies = {}
        self.headers = {k[5:]: v for k, v in environ.items() if k.startswith("HTTP_")}
        self.settings = {}
        self.kwargs = {}  # параметры запроса из path convercor

        self._fill_post_params(environ["wsgi.input"])  # request.POST & request.FILES
        self._fill_get_params(environ["QUERY_STRING"])  # request.GET

    @staticmethod
    def _prepare_url(url: str):
        return url if url.endswith("/") else url + "/"

    def _fill_get_params(self, raw_params: str):
        self.GET = {
            k: v if len(v) == 1 else v[0] for k, v in parse_qs(raw_params).items()
        }

    def _fill_post_params(self, raw_params: bytes):
        content_type = self.environ.get("CONTENT_TYPE")
        content_length = int(
            self.environ.get("CONTENT_LENGTH")
            if bool(self.environ.get("CONTENT_LENGTH"))
            else 0
        )

        match content_type:
            case "application/x-www-form-urlencoded":  # Если это обычная форма
                body = raw_params.read(content_length).decode("utf-8")
                self.POST = {
                    k: v[0] if len(v) == 1 else v for k, v in parse_qs(body).items()
                }

            case "multipart/form-data":
                form = cgi.FieldStorage(
                    fp=raw_params,
                    environ=self.environ,
                    keep_blank_values=True,
                )

                for key in form:
                    if form[key].filename:
                        # Элемент является файлом
                        self.FILES[key] = form[key]
                    else:
                        # Элемент является обычным полем
                        self.POST[key] = form[key].value
