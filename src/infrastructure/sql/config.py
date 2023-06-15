import os

from pydantic import BaseConfig, BaseSettings
from dotenv import load_dotenv

load_dotenv()


class AsyncDatabaseSettings(BaseSettings):
    user: str
    password: str
    db: str
    debug: bool = True

    class Config(BaseConfig):
        env_prefix = "postgres_"

    @property
    def host(self):
        if os.getenv("DOCKER"):
            return "db:5432"
        return "localhost:5432"

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db}"
