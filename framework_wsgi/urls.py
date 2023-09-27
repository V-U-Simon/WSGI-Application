from typing import Callable, Type
from dataclasses import dataclass

from framework_wsgi.views import View


@dataclass
class Url:
    url: str
    view: Type[View]
