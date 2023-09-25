from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from framework_wsgi.http.response import Response

path = Path("")
loader = FileSystemLoader(path)

env = Environment(
    loader=loader,
    autoescape=select_autoescape(
        "html",
    ),
    extensions=[],
)


def render(request, template_name, context={}, **kwargs) -> Response:
    # получаем шаблон
    template = env.get_template(template_name)
    # рендерим шаблон с параметрами
    str_body = template.render(context)

    Response(request=request, body=str_body)
