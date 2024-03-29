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
    YANDEX_USERINFO_ENDPOINT = 'https://login.yandex.ru/info'
    YANDEX_ACCESS_TOKEN_URL = 'https://oauth.yandex.ru/token'
    YANDEX_AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'

    VK_CLIENT_ID: str | None
    VK_CLIENT_SECRET: str | None
    VK_ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'
    VK_AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
    VK_USERINFO_ENDPOINT = 'https://api.vk.com/method/users.get?fields=sex,bdate,screen_name&v=5.131'
    VK_CLIENT_KWARGS = {
        'token_placement': 'uri',
        'token_endpoint_auth_method': 'client_secret_post',
        'scope': 'email'
    }

    MAIL_CLIENT_ID: str | None
    MAIL_CLIENT_SECRET: str | None
    MAIL_AUTHORIZE_URL = 'https://oauth.mail.ru/login'
    MAIL_ACCESS_TOKEN_URL = 'https://oauth.mail.ru/token'
    MAIL_USERINFO_ENDPOINT = 'https://oauth.mail.ru/userinfo'
    MAIL_CLIENT_KWARGS = {
        'scope': 'userinfo',
        'token_placement': 'uri',
    }

    GOOGLE_CLIENT_ID: str | None
    GOOGLE_CLIENT_SECRET: str | None
    GOOGLE_ACCESS_TOKEN_URL = 'https://oauth2.googleapis.com/token'
    GOOGLE_AUTHORIZE_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
    GOOGLE_SERVER_METADATA_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    GOOGLE_CLIENT_KWARGS = {
        'scope': 'openid email profile'
    }


config = Config()
