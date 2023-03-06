import logging
from datetime import timedelta
from os import environ


class Config:
    SERVER_NAME = environ.get('SERVER_NAME')

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

    JAEGER_AGENT_PORT = int(environ.get('JAEGER_AGENT_PORT', 6831))
    JAEGER_PORT = int(environ.get('JAEGER_PORT', 16686))
    JAEGER_HOST = environ.get('JAEGER_HOST', 'localhost')

    LOGGING_LEVEL = int(environ.get('LOGGING_LEVEL', logging.DEBUG))

    SECRET_KEY = environ.get('SECRET_KEY', 'super secret key')

    YANDEX_CLIENT_ID = environ.get('YANDEX_CLIENT_ID')
    YANDEX_CLIENT_SECRET = environ.get('YANDEX_CLIENT_SECRET')

    VK_CLIENT_ID = environ.get('VK_CLIENT_ID')
    VK_CLIENT_SECRET = environ.get('VK_CLIENT_SECRET')

    MAIL_CLIENT_ID = environ.get('MAIL_CLIENT_ID')
    MAIL_CLIENT_SECRET = environ.get('MAIL_CLIENT_SECRET')

    GOOGLE_CLIENT_ID = environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = environ.get('GOOGLE_CLIENT_SECRET')
