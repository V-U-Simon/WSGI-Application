from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

path = Path("lesson_03/templates")
loader = FileSystemLoader(path)

env = Environment(
    loader=loader,
    autoescape=select_autoescape(
        "html",
    ),
    extensions=[],
)


def render(template_name, context, **kwargs):
    template = env.get_template(template_name)
    # рендерим шаблон с параметрами
    return template.render(context).encode("utf-8")
