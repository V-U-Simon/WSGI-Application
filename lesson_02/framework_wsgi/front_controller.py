from typing import Callable

from .page_controller import index_view, not_found_view

urls = {
    "/": index_view,
    "/index/": index_view,
}


def page_not_found(request):
    status = "404 Page Not Found"
    body = "404 Page Not Found".encode("utf-8")
    return status, body


def get_page(path) -> Callable:
    return urls.get(path, page_not_found)
