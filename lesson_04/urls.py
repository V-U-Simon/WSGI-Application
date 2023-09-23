from typing import Callable

import views

# Pattern: front_controllers

routes = {
    "/": views.Index(),
    "/index/": views.Index(),
    "/about/": views.About(),
    "/contact/": views.contacts_view,
}


def page_not_found(request):
    status = "404 Page Not Found"
    body = "404 Page Not Found".encode("utf-8")
    return status, body


def get_page(path) -> Callable:
    return routes.get(path, page_not_found)
