from .template_view import render_from_line, render


def index_view(request):
    context = {"path": request.path}
    template = "This is index page. With template view on path: {{path}}"
    body = render_from_line(template, context).encode("utf-8")

    return "200 OK", body
