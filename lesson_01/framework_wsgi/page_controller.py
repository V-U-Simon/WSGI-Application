from .template_view import render_from_line


def index_view(environ):
    status = "200 OK"
    headers = [
        (
            "Content-Type",
            "text/html",
        ),
    ]

    context = {"path": environ["PATH_INFO"]}
    template = "This is index page. With template view on path: {{path}}"
    body = render_from_line(template, context).encode("utf-8")

    return status, headers, body


def not_found_view(environ):
    status = "404 NOT FOUND"
    headers = [
        (
            "Content-Type",
            "text/html",
        ),
    ]

    body = "NOT FOUND".encode("utf-8")
    return status, headers, body
