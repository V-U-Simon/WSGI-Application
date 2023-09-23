def index_view(request):
    status = "200 OK"
    headers = [
        (
            "Content-Type",
            "text/html",
        ),
    ]

    body = "Hello, world! With page controller.".encode("utf-8")
    return status, headers, body


def not_found_view(request):
    status = "404 NOT FOUND"
    headers = [
        (
            "Content-Type",
            "text/html",
        ),
    ]

    body = "NOT FOUND".encode("utf-8")
    return status, headers, body
