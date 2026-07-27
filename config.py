import os
from dotenv import load_dotenv


loaded = load_dotenv()

class DB_CONFIG:

    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME")
    DB_PASS = os.getenv("DB_PASS")
    DB_PORT = os.getenv("DB_PORT")
    DB_HOST = os.getenv("DB_HOST")

    @property
    def async_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def sync_url(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

DB_SETTINGS = DB_CONFIG()