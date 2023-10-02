from typing import List, Optional, Union
from abc import ABC, abstractmethod

from framework_wsgi.design_patterns.observer_notifier import EMAILNotifier, SMSNotifier


ID = Optional[int]


# все пользователи
class Users:
    def __init__(self, name: str, id: ID = None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}(id={self.id!r})>"


class Teachers(Users):
    def __init__(self, name: str, id: ID = None):
        super().__init__(name, id)


class Students(EMAILNotifier, Users):
    def __init__(self, name: str, id: ID = None):
        super().__init__(name, id)
