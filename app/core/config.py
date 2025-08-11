import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "fastapi-boilerplate-api")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", 3014))
    APP_HOST: str = os.getenv("APP_HOST", "localhost")
    DEBUG: bool = os.getenv("DEBUG", True)
    IS_SEED_DATA_EXEC: bool = os.getenv("IS_SEED_DATA_EXEC", False)

    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME", "<EMAIL>")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "password")
    EMAIL_HOST: str = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT: int = os.getenv("EMAIL_PORT", 587)

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "postgres")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fastapi_boilerplate")

    EXAMPLE_LISTENER_INTERVAL_SECOND: int = os.getenv('EXAMPLE_LISTENER_INTERVAL_SECOND', 10)

    BASIC_AUTH_USERNAME_PASSWORD: str = os.getenv('BASIC_AUTH_USERNAME_PASSWORD')

    class Config:
        env_file = ".env"


settings = Settings()
