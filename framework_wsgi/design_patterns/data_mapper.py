from abc import ABC, abstractmethod
from typing import List, Type, TypeVar, Optional
import sqlite3

from framework_wsgi.design_patterns.query_object import SQLQuery


T = TypeVar("T")  # Для обобщенного типа


class DataMapper(ABC):
    @abstractmethod
    def insert(self, entity: T) -> None:
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        pass

    @abstractmethod
    def delete(self, entity: T) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        pass


class SQLiteDataMapper(DataMapper):
    def __init__(self, connection: sqlite3.Connection, entity_type: Type[T]):
        self.connection = connection
        self.entity_type = (
            entity_type  # Ожидается, что это класс, например User, Course и так далее
        )

    def _serialize(self, entity: T) -> dict:
        # Преобразуем объект в словарь
        return vars(entity)

    def _deserialize(self, row: dict) -> T:
        # Создаем объект из строки базы данных
        return self.entity_type(**row)

    def insert(self, entity: T) -> None:
        data = self._serialize(entity)
        table_name = self.entity_type.__name__

        query = SQLQuery(table=table_name, data=data)
        query.INSERT()

        cursor = self.connection.cursor()
        cursor.execute(str(query), data)
        entity.id = cursor.lastrowid

    def update(self, entity: T) -> None:
        data = self._serialize(entity)
        table_name = self.entity_type.__name__

        query = SQLQuery(table=table_name, data=data)
        query.UPDATE().WHERE("id=:id")

        cursor = self.connection.cursor()
        cursor.execute(str(query), data)

    def delete(self, entity: T) -> None:
        table_name = self.entity_type.__name__

        query = SQLQuery(table=table_name)
        query.DELETE().WHERE("id=:id")

        cursor = self.connection.cursor()
        cursor.execute(str(query), {"id": entity.id})
        entity.id = None

    def find_by_id(self, id: int) -> Optional[T]:
        table_name = self.entity_type.__name__

        query = SQLQuery(table=table_name)
        query.SELECT().WHERE("id=:id")

        cursor = self.connection.cursor()
        cursor.execute(str(query), {"id": id})
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Passing id:{id} is not exist in database")
        return self._deserialize(row)

    def find_all(self) -> List[T]:
        table_name = self.entity_type.__name__

        query = SQLQuery(table=table_name)
        query.SELECT()

        cursor = self.connection.cursor()
        cursor.execute(str(query))
        rows = cursor.fetchall()
        return [self._deserialize(row) for row in rows]


if __name__ == "__main__":
    from framework_wsgi.design_patterns.domain_users import Users
    import os

    # соединение с БД
    curdir = os.path.dirname(os.path.abspath(__file__))
    db_path = curdir + "/../../education.db"
    connecntion = sqlite3.connect(db_path)
    connecntion.row_factory = sqlite3.Row
    users_mapper = SQLiteDataMapper(connecntion, Users)

    # создание пользователя
    user = Users(name="John")
    print(f"create: {user}")

    # insert
    users_mapper.insert(user)
    connecntion.commit()
    print(f"insert: {user}")

    # select all
    users = users_mapper.find_all()
    print(f"select all: {users}")

    # select by id
    user = users_mapper.find_by_id(user.id)
    print(f"select by id: {user}")

    # update
    user.name = "Joe"
    users_mapper.update(user)
    connecntion.commit()
    user = users_mapper.find_by_id(user.id)
    print(f"update: {user}")

    # delete
    users_mapper.delete(user)
    connecntion.commit()
    users = users_mapper.find_all()
    print(f"delete: {users}")

    connecntion.close()
