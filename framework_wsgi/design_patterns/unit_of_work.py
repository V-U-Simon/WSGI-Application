from typing import Any, List, Optional, Type
from abc import ABC

import os
import sqlite3

from framework_wsgi.design_patterns.repository import SQLiteRepository
from framework_wsgi.design_patterns.domain_users import Users
from framework_wsgi.design_patterns import identity_map
from framework_wsgi.design_patterns.connector import ConnectorDB, DatabaseConnector


class UnitOfWork(ABC):
    def __enter__(self) -> None:
        raise NotImplementedError

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError


class SQLiteUnitOfWork:
    def __init__(self, db_connector: DatabaseConnector = ConnectorDB):
        self.connection: sqlite3.Connection | None = None
        self.db_connector = db_connector
        self.identity_map = identity_map.IdentityMap()

    def commit(self) -> None:
        self.connection.execute("COMMIT")

    def rollback(self) -> None:
        self.connection.execute("ROLLBACK")

    def __enter__(self) -> "SQLiteRepository":
        self.connection = self.db_connector.connect()
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
