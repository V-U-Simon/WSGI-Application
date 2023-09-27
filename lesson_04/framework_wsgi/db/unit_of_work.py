from typing import Any, List, Optional, Type
from abc import ABC

import os
import sqlite3

from framework_wsgi.db.repository import SQLiteRepository
from framework_wsgi.db.domain import Users
from framework_wsgi.db import identity_map


class UnitOfWork(ABC):
    def __enter__(self) -> None:
        raise NotImplementedError

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError


def connection_factory_sqlite(db_path: str = None) -> sqlite3.Connection:
    if db_path is None:
        db_path = os.path.dirname(os.path.abspath(__file__)) + "/../../education.db"
    return sqlite3.connect(db_path)


class SQLiteUnitOfWork:
    def __init__(self, connection_factory=connection_factory_sqlite):
        self.connection: sqlite3.Connection | None = None
        self.create_connection = connection_factory
        self.identity_map = identity_map.IdentityMap()

    def commit(self) -> None:
        self.connection.execute("COMMIT")

    def rollback(self) -> None:
        self.connection.execute("ROLLBACK")

    def __enter__(self) -> "SQLiteRepository":
        self.connection = self.create_connection()
        self.connection.execute("BEGIN")
        return SQLiteRepository(self.connection, self.identity_map)

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.connection.close()
        self.identity_map.clear()


if __name__ == "__main__":
    uow = SQLiteUnitOfWork()

    # Корректная транзакция
    with uow as repo:
        users = repo(Users).all()
        print(users)

        user = Users(name="Mike")
        repo.save(user)
        print(f"{user}")

        user.name = "Mikki"
        repo.save(user)
        print(f"{user}")

        users = repo(Users).all()
        print(users)

        repo.delete(user)
        print(f"{user}")

    # Порочная транзакция
    try:
        with uow as repo:
            users = repo(Users).all()
            print(users)

            user = Users(name="ErrorNameForExample")
            repo.save(user)
            print(f"{user}")
            raise sqlite3.OperationalError

    except sqlite3.OperationalError:
        # Проверяем налчие пользователя в БД с именем ErrorNameForExample
        with uow as repo:
            users = repo(Users).all()
            print(users)
