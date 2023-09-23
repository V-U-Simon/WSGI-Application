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