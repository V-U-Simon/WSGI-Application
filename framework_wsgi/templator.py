from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from framework_wsgi.http.response import Response, Request


class TemplateEngine:
    def __init__(self, settings: dict):
        self.base_dir = settings.get("BASE_DIR", ".")
        self.template_dir = settings.get("TEMPLATES_DIR", "")
        self.path = Path(self.base_dir, self.template_dir)

        if not self.path.exists:
            Exception("Template directory does not exist")

    def apply(self):
        return Environment(
            loader=FileSystemLoader(self.path),
            autoescape=select_autoescape(
                "html",
            ),
            extensions=[],
        )


def render(request: Request, template_name, context={}, **kwargs) -> Response:
    engine = TemplateEngine(request.settings)

    if not Path(engine.path, template_name).exists():
        Exception(f"Template {template_name} does not exist")

    env = engine.apply()

    # получаем шаблон
    template = env.get_template(template_name)
    # рендерим шаблон с параметрами
    str_body = template.render(context)

    return Response(request=request, body=str_body)
