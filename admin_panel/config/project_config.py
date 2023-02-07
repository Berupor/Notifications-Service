"""Settings"""

import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = os.path.join(BASE_DIR, "..")


class DjangoSettings(BaseSettings):
    secret_key: str


class PostgresSettings(BaseSettings):
    user: str
    dbname: str
    password: str
    host: str
    port: int


class Settings(BaseSettings):
    django: DjangoSettings
    postgres: PostgresSettings

    class Config:
        #  For local development outside of docker
        env_file = (
            os.path.join(ENV_DIR, ".env"),
            os.path.join(ENV_DIR, ".env.dev"),
        )
        env_nested_delimiter = "__"


settings = Settings()
