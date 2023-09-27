from typing import Dict, Optional


class SQLQuery:
    def __init__(self, table: str, data: Optional[Dict[str, object]] = None):
        self.table = table
        self.query: str = ""

        if data:
            self.columns = ", ".join(data.keys())
            self.placeholders = [f":{key}" for key in data.keys()]
            self.values = ", ".join(self.placeholders)
            self.update_values = ", ".join(
                [f"{col}=:{col}" for col in self.columns.split(", ")]
            )
        else:
            self.columns = ""
            self.placeholders = []
            self.values = ""
            self.update_values = ""

    def INSERT(self) -> "SQLQuery":
        if self.columns:
            self.query += f"INSERT INTO {self.table} ({self.columns}) "
            self.query += f"VALUES ({self.values}) "
        return self

    def UPDATE(self) -> "SQLQuery":
        if self.update_values:
            self.query += f"UPDATE {self.table} SET "
            self.query += f"{self.update_values} "
        return self

    def DELETE(self) -> "SQLQuery":
        self.query += f"DELETE FROM {self.table} "
        return self

    def WHERE(self, condition: str) -> "SQLQuery":
        self.query += f"WHERE {condition} "
        return self

    def SELECT(self) -> "SQLQuery":
        self.query += f"SELECT * FROM {self.table} "
        return self

    def __str__(self) -> str:
        return self.query.strip()


if __name__ == "__main__":
    data = {"name": "John", "email": "john@email.com"}

    query = SQLQuery(table="users", data=data)
    query.INSERT()
    print(query)  # INSERT INTO users (name, email) VALUES (:name, :email)

    query = SQLQuery(table="users", data=data)
    query.UPDATE().WHERE("id=:id")
    print(str(query))  # UPDATE users SET name=:name, email=:email WHERE id=:id

    query = SQLQuery(table="users")
    query.DELETE().WHERE("id=:id")
    print(str(query))  # DELETE FROM users WHERE id=:id

    query = SQLQuery(table="users")
    query.SELECT().WHERE("id=:id")
    print(str(query))  # SELECT * FROM users WHERE id=:id
