# src/core/config.py
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    # Добавляем новые настройки
    SYSTEM_USERNAME: str = "system"
    INITIAL_ROLE_CREATED_BY: str = "system"
    INITIAL_USER_CREATED_BY: str = "system"

    # Тестовый суперпользователь
    INITIAL_USER_TOKEN: str = "8c6256c0-9db7-4e0d-ba61-1dee5eea40aa"
    INITIAL_USER_USERNAME: str = "admin"
    INITIAL_USER_EMAIL: str = "admin@example.com"
    INITIAL_USER_PHONE: str = "+79998887766"
    INITIAL_USER_PASSWORD: str = "SuperSecret123!"
    INITIAL_USER_ROLE: str = "FULL_ACCESS"

    # Данные для postgres
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "pass"
    POSTGRES_DB: str = "dbname"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: str = "5432"

    # Keys for token
    SECRET_KEY: str = "your-256-bit-secret"  # Минимум 32 символа
    ALGORITHM: str = "HS256"  # Или другой алгоритм (например, RS256)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ENV: str = "dev"

    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False
    DB_MODE: str = "mock"

    @property
    def SYNC_DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def ASYNC_DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
