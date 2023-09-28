import os


class Settings:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_ENGINE = "sqlite"
    DB_SQLite_FILE = BASE_DIR + "/education.db"

    TEMPLATES_DIR = "templates"
    DEFAULT_HEADERS = {
        "Content-Type": "text/html",
        # "Content-Type": "application/json",
    }
