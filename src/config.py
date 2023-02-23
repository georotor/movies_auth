import logging
from datetime import timedelta
from os import environ


class Config:
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

    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY', 'super secret')
    JWT_TOKEN_LOCATION = 'headers'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(weeks=4)

    RESTX_MASK_SWAGGER = False

    REDIS_HOST = environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(environ.get('REDIS_PORT', 6379))
    REDIS_DECODE_RESPONSES = True

    LOGGING_LEVEL = int(environ.get('LOGGING_LEVEL', logging.DEBUG))
