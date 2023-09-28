from abc import ABC
import os
import sqlite3
from typing import Any
from framework_wsgi.design_patterns.connector import ConnectorDB

from framework_wsgi.design_patterns.data_mapper import SQLiteDataMapper, DataMapper
from framework_wsgi.design_patterns.domain_users import Students
from framework_wsgi.design_patterns.mapper_registry import MapperRegistry
from framework_wsgi.design_patterns import identity_map

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

    def __init__(self, connection: sqlite3.Connection, identity_map):
        self.connection = connection
        self.identity_map = identity_map
        self.current_mapper: DataMapper | None = None

    def __call__(self, entity_type):
        """Получение маппера (что-то вроде выбора таблицы в репозитории)"""
        if entity_type not in self._registry:
            raise AttributeError(
                f"No mapper registered for entity: {entity_type.__name__}"
            )
        self.current_mapper = SQLiteDataMapper(self.connection, entity_type)
        return self

    def save(self, entity: T) -> None:
        entity_type = type(entity)
        mapper = SQLiteDataMapper(self.connection, entity_type)
        if not entity.id:
            mapper.insert(entity)
            self.identity_map.add(entity_type, entity.id, entity)
        else:
            mapper.update(entity)
            self.identity_map.update(entity_type, entity.id, entity)

    def delete(self, entity: T) -> None:
        entity_type = type(entity)
        mapper = SQLiteDataMapper(self.connection, entity_type)
        mapper.delete(entity)
        self.identity_map.remove(entity_type, entity.id)

    def find_by_id(self, id: int) -> Optional[T]:
        entity = self.identity_map.get(self.current_mapper.entity_type, id)
        if entity is None:
            entity = self.current_mapper.find_by_id(id)
            if entity:
                self.identity_map.add(self.current_mapper.entity_type, id, entity)
                print(f"Identity mapping: get {entity} from stash")
        return entity

    def all(self) -> List[T]:
        entities = self.current_mapper.find_all()
        for entity in entities:
            self.identity_map.add(self.current_mapper.entity_type, entity.id, entity)
            print(f"Identity mapping: get {entity} from stash")
            return entities


if __name__ == "__main__":
    # соединение с БД
    connection = ConnectorDB.connect()
    repo = SQLiteRepository(connection, identity_map.IdentityMapStub())

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
