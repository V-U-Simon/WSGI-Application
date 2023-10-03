import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from framework_wsgi.http.response import Response, Request


def get_template_env(settings):
    path = settings.TEMPLATES_DIR

    return Environment(
        loader=FileSystemLoader(path),
        autoescape=select_autoescape(
            "html",
        ),
        extensions=[],
    )


def render(request: Request, template_name, context={}, *args, **kwargs) -> Response:
    env = get_template_env(request.settings)

    # if not Path(env.path, template_name).exists():
    #     Exception(f"Template {template_name} does not exist")

    template = env.get_template(template_name)  # получаем шаблон
    template.globals[
        "static"
    ] = request.settings.STATIC_URL  # добавляем url к static файлам
    context.update({"request": request})
    str_body = template.render(context)  # рендерим шаблон с параметрами
    response = Response(request=request, body=str_body)
    response.headers.update({"Content-Type": "text/html"})
    return response


class TemplateEngine:
    def __init__(self) -> None:
        pass

    def build(self) -> str:
        pass


class TemplateEngineHTML:
    def __init__(
        self, request: Request, template_name: str, context: dict = {}, *args, **kwargs
    ) -> None:
        self.env = get_template_env(request.settings)
        self.template_name = template_name
        self.context = context
        self.context.update({"request": request})
        self.static_url = request.settings.STATIC_URL
        request.response_headers = {"Content-Type": "text/html"}

    def render(self) -> str:
        template = self.env.get_template(self.template_name)  # получаем шаблон
        template.globals["static"] = self.static_url  # добавляем url к static файлам
        str_body = template.render(self.context)  # рендерим шаблон с параметрами
        return str_body


import json
from framework_wsgi.http.response import Response, Request


class TemplateEngineJSON:
    def __init__(self, request, context: dict = {}, *args, **kwargs) -> None:
        self.context = context
        request.response_headers = {"Content-Type": "application/json"}

    def render(self) -> str:
        json_compatible_context = self.complex_to_dict(self.context)
        json_body = json.dumps(json_compatible_context)
        return json_body

    @staticmethod
    def complex_to_dict(obj, visited=None):
        if visited is None:
            visited = set()

        if id(obj) in visited:
            return None  # Циклическая ссылка

        visited.add(id(obj))

        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj

        if isinstance(obj, list):
            return [TemplateEngineJSON.complex_to_dict(e, visited) for e in obj]

        if isinstance(obj, dict):
            return {
                key: TemplateEngineJSON.complex_to_dict(value, visited)
                for key, value in obj.items()
            }

        obj_dict = obj.__dict__.copy()
        for key, value in obj_dict.items():
            obj_dict[key] = TemplateEngineJSON.complex_to_dict(value, visited)

        return obj_dict
