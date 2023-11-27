from framework_wsgi.templator import render
from framework_wsgi.http.response import Response
from urls import Router


@Router("/about/")
def about(request) -> Response:
    return render(request, "about.html")
