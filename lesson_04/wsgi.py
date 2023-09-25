import os
from wsgiref.simple_server import make_server
from framework_wsgi.app import Application
from framework_wsgi.middleware import middlewares
from urls import urlpatterns


settings = {
    "BASE_DIR": os.path.dirname(os.path.abspath(__file__)),
    "TEMPLATES_DIR": "templates",
    "DEFAULT_HEADERS": {
        "Content-Type": "text/html",
        # "Content-Type": "application/json",
    },
}


application = Application(
    urls=urlpatterns,
    middlewares=middlewares,
    settings=settings,
)


if __name__ == "__main__":
    with make_server(host="", port=8000, app=application) as httpd:
        print(f"run wsgi server from {os.curdir}")
        print("Serving on http://localhost:8000...")
        httpd.serve_forever()
