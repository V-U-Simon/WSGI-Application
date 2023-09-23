from jinja2 import Template


def render_from_line(template_line: str, context: dict) -> str:
    """Сформировать шаблон из текста"""
    template = Template(template_line)  # 📝 ✅ создаем  шаблон
    return template.render(**context)  # 📝 👀 рендерим шаблон (используя контекст)
