from typing import Callable

from views import index_view, contacts_view

# Pattern: front_controllers

urls = {
    "/": index_view,
    "/index/": index_view,
    "/contact/": contacts_view,
}


def page_not_found(request):
    status = "404 Page Not Found"
    body = "404 Page Not Found".encode("utf-8")
    return status, body


def get_page(path) -> Callable:
    return urls.get(path, page_not_found)
