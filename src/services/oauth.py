import logging
from functools import lru_cache

from authlib.integrations.flask_client import OAuth
from models.user import User
from services.user import UserService

logger = logging.getLogger(__name__)


class OAuthError(Exception):
    """Исключение для ошибок при аутентификации."""


class OAuthService:
    def __init__(self, oauth: OAuth, user_service: UserService):
        self.oauth = oauth
        self.user_service = user_service

    def get_auth_url(self, provider: str, authorization_endpoint: str) -> tuple | None:
        """
        Подготовка ссылки для авторизации через внешний сервис
        :param provider: Название сервиса
        :param authorization_endpoint: Callback ссылка для сервиса авторизации
        """
        client = self.oauth.create_client(provider)
        if not client:
            return None

        rv = client.create_authorization_url(authorization_endpoint)
        client.save_authorize_data(redirect_uri=authorization_endpoint, **rv)

        return rv

    def authorize(self, provider: str):
        """
        Авторизация через внешний сервис.
        Если в системе уже есть пользователь с email'ом авторизующегося, то он будет "подключен" к существующему
        аккаунту, иначе будет создан новый аккаунт со случайным паролем.

        :param provider: Название сервиса.
        :return: Объект пользователя.
        """
        client = self.oauth.oauth2_client_cls = self.oauth.create_client(provider)
        if not client:
            return None

        token = client.authorize_access_token()
        userinfo = client.userinfo()

        data = {
            'token': token,
            'userinfo': userinfo
        }

        email = client.server_metadata['get_email'](data)
        social_id = str(client.server_metadata['get_social_id'](data))

        if email is None:
            raise OAuthError("Email required")

        user = self.user_service.find_user_by_social(social_id=social_id, social_name=provider)
        if user:
            return user

        user = self.user_service.registration_social(
            email=email, social_id=social_id, social_name=provider
        )

        return user


@lru_cache()
def get_oauth_service(oauth: OAuth, user_service: UserService) -> OAuthService:
    return OAuthService(oauth, user_service)
