from . import page_controller
from . import front_controller


def application(environ: dict, start_response):
    view = front_controller.get_page(environ["PATH_INFO"])
    status, headers, body = view(environ)

    start_response(status, headers)  # отправляем заголовки клиенту
    return [
        body
    ]  # отправляем итерируемый объект (т.к. тело может быть слишком большим)
