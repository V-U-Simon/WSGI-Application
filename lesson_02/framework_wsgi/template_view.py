from os.path import join
from jinja2 import Template


def render_from_line(template_line: str, context: dict) -> str:
    """Сформировать шаблон из текста"""
    template = Template(template_line)  # 📝 ✅ создаем  шаблон
    return template.render(**context)  # 📝 👀 рендерим шаблон (используя контекст)


def render(template_name, context: dict = {}, **kwargs):
    folder = "lesson_02/templates"
    file_path = join(folder, template_name)
    # print(file_path)

    # Открываем шаблон по имени
    with open(file_path, encoding="utf-8") as f:
        # Читаем
        template = Template(f.read())

    # рендерим шаблон с параметрами
    context.update(**kwargs)
    return template.render(**context).encode("utf-8")


if __name__ == "__main__":
    body = render(
        "index.html",
        context={"path": "test"},
    )
    print(body)
