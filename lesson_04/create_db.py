import os
import sqlite3


def execute_sql_script(filename: str, db_name: str):
    # Чтение SQL-скрипта
    with open(filename, "r") as file:
        sql_script = file.read()

    # Подключение к базе данных
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        # Выполнение SQL-скрипта
        cursor.executescript(sql_script)
        conn.commit()
        print("database is created successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Закрытие соединения с базой данных
        conn.close()


if __name__ == "__main__":
    # Вызов функции для выполнения SQL-скрипта и создания таблиц
    curdir = os.path.dirname(os.path.abspath(__file__))
    execute_sql_script(curdir + "/create_db.sql", curdir + "/education.db")
