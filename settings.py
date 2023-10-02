import os
from pathlib import Path


class Settings:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_ENGINE = "sqlite"
    DB_SQLite_FILE = BASE_DIR + "/education.db"

    TEMPLATES_DIR = Path(BASE_DIR, "templates")

    DEFAULT_HEADERS = {
        "Content-Type": "text/html",
        # "Content-Type": "application/json",
    }

    if not TEMPLATES_DIR.exists:
        Exception("Template directory does not exist")

    STATIC_DIR_NAME = "staticfiles"
    STATIC_URL = "/static/"


# print(Settings.TEMPLATES_DIR)
