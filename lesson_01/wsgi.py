from wsgiref.simple_server import make_server


def application(environ: dict, start_response):
    # ...бизнес-логика...

    status = "200 OK"
    headers = [
        (
            "Content-Type",
            "text/html",
        ),
    ]
    body = "Hello, world!".encode("utf-8")

    start_response(status, headers)  # отправляем заголовки клиенту
    return [body]  # отправляем итерируемый объект (т.к. тело может быть слишком большим)


if __name__ == "__main__":
    with make_server(host="", port=8000, app=application) as httpd:
        print("Serving on http://localhost:8000...")
        httpd.serve_forever()