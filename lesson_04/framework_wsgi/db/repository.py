from abc import ABC
import os
import sqlite3
from typing import Any

from framework_wsgi.db.data_mapper import SQLiteDataMapper, DataMapper
from framework_wsgi.db.domain import Students
from framework_wsgi.db.mapper_registry import MapperRegistry


from abc import ABC, abstractmethod
from typing import TypeVar, List, Optional

T = TypeVar("T")


class RepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: T) -> None:
        """Сохраняет или обновляет сущность (если уже есть) в базе данных."""

    @abstractmethod
    def delete(self, entity: T) -> None:
        """Удаляет сущность из базы данных."""

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[T]:
        """Возвращает сущность по её ID."""

    @abstractmethod
    def all(self) -> List[T]:
        """Возвращает все сущности."""


class SQLiteRepository:
    _registry = MapperRegistry.registry

    def __init__(self, connecntion: sqlite3.Connection):
        self.connecntion = connecntion
        self.connecntion.row_factory = sqlite3.Row
        self.current_mapper: DataMapper | None = None

    def __call__(self, entity_type):
        """Получение маппера (что-то вроде выбора таблицы в репозитории)"""
        if entity_type not in self._registry:
            raise AttributeError(
                f"No mapper registered for entity: {entity_type.__name__}"
            )
        self.current_mapper = SQLiteDataMapper(self.connecntion, entity_type)
        return self

    def save(self, entity: T) -> None:
        mapper = SQLiteDataMapper(self.connecntion, type(entity))
        if not entity.id:
            mapper.insert(entity)
        else:
            mapper.update(entity)

    def delete(self, entity: T) -> None:
        mapper = SQLiteDataMapper(self.connecntion, type(entity))
        mapper.delete(student)

    def find_by_id(self, id: int) -> Optional[T]:
        return self.current_mapper.find_by_id(id)

    def all(self) -> List[T]:
        return self.current_mapper.find_all()


if __name__ == "__main__":
    # соединение с БД

    curdir = os.path.dirname(os.path.abspath(__file__))
    connection = sqlite3.connect(curdir + "/../../education.db")
    repo = SQLiteRepository(connection)

    # создание пользователя
    student = Students(name="John")
    print(f"create: {student}")

    # insert
    repo.save(student)
    connection.commit()
    print(f"insert: {student}")

    # update
    student.name = "Joe"
    repo.save(student)
    connection.commit()
    print(f"update: {student}")

    # select by id
    print(student.id)
    student = repo(Students).find_by_id(student.id)
    print(f"select by id: {student}")

    # delete
    repo.delete(student)
    connection.commit()
    print(f"delete: {student}")

    # select all
    students = repo(Students).all()
    print(f"select all: {students}")

    connection.close()
