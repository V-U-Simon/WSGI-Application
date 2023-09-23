from framework_wsgi.middleware import middleware


class Request:
    def __init__(self, environ: dict):
        print(f"Processing request")
        self.environ = environ
        self.path = environ["PATH_INFO"]

        for func in middleware.pre_process_funcs:
            func(self)


@middleware.pre_process
def check_path_slash(request: Request):
    if not request.path.endswith("/"):
        request.path = request.path + "/"
