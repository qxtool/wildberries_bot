import os

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv.load_dotenv()


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(__file__)
    DEBUG: bool = False

    TELEGRAM_TOKEN: str
    BASE_URL: str
    HOST: str
    PORT: int

    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    TIME_ZONE: str = "UTC"

    @property
    def WEBHOOK_PATH(self) -> str:
        return f"/{self.TELEGRAM_TOKEN}"

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.BASE_URL}{self.WEBHOOK_PATH}"

    @property
    def POSTGRES_URL_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
