from abc import ABC, abstractmethod
from typing import List, Type, TypeVar, Optional

import sqlite3
from typing import List, Type

T = TypeVar("T")  # Для обобщенного типа


class DataMapperInterface(ABC):
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


class SQLiteDataMapper(DataMapperInterface):
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
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f":{key}" for key in data.keys()])
        query = f"INSERT INTO {self.entity_type.__name__} ({columns}) VALUES ({placeholders})"
        cursor = self.connection.cursor()
        cursor.execute(query, data)
        self.connection.commit()

        entity.id = cursor.lastrowid  # Устанавливаем ID после вставки

    def update(self, entity: T) -> None:
        data = self._serialize(entity)
        set_clause = ", ".join([f"{key}=:{key}" for key in data.keys() if key != "id"])
        query = f"UPDATE {self.entity_type.__name__} SET {set_clause} WHERE id=:id"
        cursor = self.connection.cursor()
        cursor.execute(query, data)
        self.connection.commit()

    def delete(self, entity: T) -> None:
        query = f"DELETE FROM {self.entity_type.__name__} WHERE id=:id"
        cursor = self.connection.cursor()
        cursor.execute(query, {"id": entity.id})
        self.connection.commit()

    def find_by_id(self, id: int) -> Optional[T]:
        query = f"SELECT * FROM {self.entity_type.__name__} WHERE id=:id"
        cursor = self.connection.cursor()
        cursor.execute(query, {"id": id})
        self.connection.commit()
        row = cursor.fetchone()
        return self._deserialize(row) if row else None

    def find_all(self) -> List[T]:
        query = f"SELECT * FROM {self.entity_type.__name__}"
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        rows = cursor.fetchall()
        return [self._deserialize(row) for row in rows]


if __name__ == "__main__":
    from framework_wsgi.db.domain import Users, Courses
    import os

    # соединение с БД
    curdir = os.path.dirname(os.path.abspath(__file__))
    db_path = curdir + "/../../education.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    users_mapper = SQLiteDataMapper(conn, Users)

    # создание пользователя
    user = Users(name="John")
    print(f"create: {user}")

    # insert
    users_mapper.insert(user)
    conn.commit()
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
    user = users_mapper.find_by_id(user.id)
    print(f"update: {user}")

    # delete
    users_mapper.delete(user)
    users = users_mapper.find_all()
    print(f"delete: {users}")

    conn.close()
