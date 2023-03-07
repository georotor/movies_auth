import logging
from datetime import timedelta
from os import environ

from pydantic import BaseSettings


class Config(BaseSettings):
    SERVER_NAME: str | None

    PROPAGATE_EXCEPTIONS = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        environ.get('POSTGRES_USER', 'app'),
        environ.get('POSTGRES_PASSWORD', '123qwe'),
        environ.get('POSTGRES_HOST', 'localhost'),
        int(environ.get('POSTGRES_PORT', 5432)),
        environ.get('POSTGRES_DB', 'auth_database')
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY: str = 'super secret'
    JWT_TOKEN_LOCATION = 'headers'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(weeks=4)

    RESTX_MASK_SWAGGER = False

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DECODE_RESPONSES = True

    JAEGER_AGENT_PORT: int = 6831
    JAEGER_HOST: str = 'localhost'
    JAEGER_ENABLE: bool = True

    LOGGING_LEVEL: int = logging.DEBUG

    SECRET_KEY: str = 'super secret key'

    YANDEX_CLIENT_ID: str | None
    YANDEX_CLIENT_SECRET: str | None

    VK_CLIENT_ID: str | None
    VK_CLIENT_SECRET: str | None

    MAIL_CLIENT_ID: str | None
    MAIL_CLIENT_SECRET: str | None

    GOOGLE_CLIENT_ID: str | None
    GOOGLE_CLIENT_SECRET: str | None


config = Config()
