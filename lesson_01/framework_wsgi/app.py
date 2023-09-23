from . import page_controller


def application(environ: dict, start_response):
    status, headers, body = page_controller.index_view(environ)

    start_response(status, headers)  # отправляем заголовки клиенту
    return [
        body
    ]  # отправляем итерируемый объект (т.к. тело может быть слишком большим)
