from framework_wsgi.middleware import middleware
from urllib.parse import parse_qs
import cgi


class Request:
    def __init__(self, environ: dict):
        print(f"Processing request")
        self.environ = environ
        self.path = environ["PATH_INFO"]
        self.method = environ["REQUEST_METHOD"].upper()
        self.params = {}
        self.data = {}

        for func in middleware.pre_process_funcs:
            func(self)


@middleware.pre_process
def check_path_slash(request: Request):
    # добавление закрывающего слеша
    if not request.path.endswith("/"):
        request.path = request.path + "/"


@middleware.pre_process
def parse_request_data(request: Request):
    # Для GET-запросов
    if request.method == "GET":
        query_string = request.environ.get("QUERY_STRING", "")
        request.GET = {
            k: v[0] if len(v) == 1 else v for k, v in parse_qs(query_string).items()
        }

    # Для POST-запросов
    elif request.method == "POST":
        content_type = request.environ.get("CONTENT_TYPE")
        content_length = int(request.environ.get("CONTENT_LENGTH", 0))

        # Если это обычная форма
        if content_type == "application/x-www-form-urlencoded":
            body = request.environ["wsgi.input"].read(content_length).decode("utf-8")
            request.POST = {
                k: v[0] if len(v) == 1 else v for k, v in parse_qs(body).items()
            }

        # Если это multipart/form-data
        elif content_type.startswith("multipart/form-data"):
            form = cgi.FieldStorage(
                fp=request.environ["wsgi.input"],
                environ=request.environ,
                keep_blank_values=True,
            )

            for key in form:
                if form[key].filename:
                    # Элемент является файлом
                    request.FILES[key] = form[key]
                else:
                    # Элемент является обычным полем
                    request.POST[key] = form[key].value
