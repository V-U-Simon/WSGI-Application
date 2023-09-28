from abc import ABC, abstractmethod, abstractclassmethod
import sqlite3
from settings import Settings


class DatabaseConnector(ABC):
    @abstractclassmethod
    def connect(self):
        pass

    @abstractclassmethod
    def close(self):
        pass


class SQLiteConnector(DatabaseConnector):
    @classmethod
    def connect(cls, db_name=None):
        db_name = db_name if db_name else cls.db_name
        cls.connection = sqlite3.connect(db_name)
        cls.connection.row_factory = sqlite3.Row
        return cls.connection

    @classmethod
    def close(cls):
        cls.connection.close()


def _get_end_setup_connetor(db_engine: DatabaseConnector = Settings.DB_ENGINE):
    match db_engine.lower():
        case "sqlite":
            connector = SQLiteConnector
            connector.db_name = Settings.DB_SQLite_FILE

    return connector


ConnectorDB = _get_end_setup_connetor()

if __name__ == "__main__":
    connection_1 = ConnectorDB.connect()
    connection_2 = ConnectorDB.connect()
    connection_3 = ConnectorDB.connect()
    print(connection_1)
    print(connection_2)
    print(connection_3)
