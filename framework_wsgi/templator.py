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
    str_body = template.render(context)  # рендерим шаблон с параметрами
    return Response(request=request, body=str_body)


class TemplateEngine:
    def __init__(self) -> None:
        pass

    def build(self) -> str:
        pass


class TemplateEngineHTML:
    def __init__(
        self, request: Request, template_name, context={}, *args, **kwargs
    ) -> None:
        self.env = get_template_env(request.settings)
        self.template_name = template_name
        self.context = context

    def render(self) -> str:
        template = self.env.get_template(self.template_name)  # получаем шаблон
        str_body = template.render(self.context)  # рендерим шаблон с параметрами
        return str_body
