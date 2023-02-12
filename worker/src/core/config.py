"""Settings"""

import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = os.path.join(BASE_DIR, "..", "..")


class FastapiSettings(BaseSettings):
    project_name: str
    secret_key: str
    host: str
    port: int


class RabbitMQSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str


class PostgresSettings(BaseSettings):
    user: str
    dbname: str
    password: str
    host: str
    port: int


class EmailServer(BaseSettings):
    host: str
    port: int


class ClickhouseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str


class Settings(BaseSettings):
    token_algo: str

    rabbitmq: RabbitMQSettings
    fastapi: FastapiSettings
    postgres: PostgresSettings
    email_server: EmailServer
    clickhouse: ClickhouseSettings

    class Config:
        #  For local development outside of docker
        env_file = (
            os.path.join(ENV_DIR, ".env"),
            os.path.join(ENV_DIR, ".env.dev"),
        )
        env_nested_delimiter = "__"


settings = Settings()
