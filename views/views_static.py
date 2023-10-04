import os
from pathlib import Path
from framework_wsgi.content_map import CONTENT_TYPES_MAP
from framework_wsgi.http.request import Request
from framework_wsgi.http.response import Response
from framework_wsgi.views import View


class StaticProcessor(View):
    def get_content_type(self, file: str) -> str:
        file_name = os.path.basename(file).lower()  # styles.css
        extension = os.path.splitext(file_name)[1]  # .css
        content_type = CONTENT_TYPES_MAP.get(extension, "text/html")

        return f"{content_type}; charset=UTF-8"

    def get(self, request: Request, *args, **kwargs) -> Response:
        static_dir = request.settings.STATIC_DIR_NAME
        static_file = request.environ.get("PATH_INFO").replace("/static/", "")
        static_file = static_file.split("/")
        root_path = request.settings.BASE_DIR

        file_name = Path(root_path) / static_dir
        for file in static_file:
            file_name = file_name / file

        with open(file_name, "rb") as f:
            body = f.read()

        headers = {"Content-Type": self.get_content_type(static_file[-1])}

        response = Response(request)
        response.headers.update(headers)
        response.body = body

        return response
