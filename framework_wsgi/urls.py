import re
from dataclasses import dataclass
from typing import Type, Callable, Dict, Optional

from framework_wsgi.views import View


@dataclass
class Url:
    url: str
    view: Type[View]

    def __post_init__(self):
        self.url = self.convert_path_to_regex(self.url)

    @staticmethod
    def convert_path_to_regex(path: str) -> str:
        path = re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path)
        return f"^{path}$"

    def match(self, request_url: str) -> Optional[Dict[str, str]]:
        match = re.match(self.url, request_url)
        if match:
            return match.groupdict()
        return None
