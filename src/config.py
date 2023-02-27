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

    LOGGING_LEVEL = int(environ.get('LOGGING_LEVEL', logging.DEBUG))

    SECRET_KEY = environ.get('SECRET_KEY', 'super secret key')

    YANDEX_CLIENT_ID = 'f71587727e5e43978e62fd58ee1212e9'
    YANDEX_CLIENT_SECRET = '91fe86ef7b4c489f995d90fcec8dc138'

    VK_CLIENT_ID = '51566471'
    VK_CLIENT_SECRET = 'RVyc9VqbVvDxkDiHgiOp'

    OK_CLIENT_ID = '512001772843'
    OK_CLIENT_SECRET = '6582C35649161446DE632220'

    MAIL_CLIENT_ID = '68799f29312f4ce0bfafcdb9ab50f62d'
    MAIL_CLIENT_SECRET = 'a2bd8e24bfad47bca1cca64c445d81f1'
