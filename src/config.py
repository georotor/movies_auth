from datetime import timedelta
from os import environ

# from pydantic import BaseSettings
#
#
# class DataBases(BaseSettings):
#     postgres_password: str = '123qwe'
#     postgres_user: str = 'app'
#     postgres_db: str = 'auth_database'
#     postgres_host: str = 'localhost'
#     postgres_port: int = 5432
#
#     redis_host: str = 'localhost'
#     redis_port: int = 6379
#
#     class Config:
#         env_nested_delimiter = '__'
#
#
# # config = Config()


class Config:
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

    REDIS_HOST = environ.get('REDIS_HOST', 'redis://default:redispw@localhost')
    REDIS_PORT = environ.get('REDIS_PORT', '49153')
