from typing import Callable

from page_controller import index_view, not_found_view

urls = {
    "/": index_view,
    "/index/": index_view,
}


def get_page(path) -> Callable:
    if not path.endswith("/"):
        path += "/"

    return urls.get(path, not_found_view)
