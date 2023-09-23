from wsgiref.simple_server import make_server
from framework_wsgi import app

application = app.application

if __name__ == "__main__":
    with make_server(host="", port=8000, app=application) as httpd:
        print("Serving on http://localhost:8000...")
        httpd.serve_forever()
