import logging
from functools import lru_cache

from authlib.integrations.flask_client import OAuth
from services.user import UserService

logger = logging.getLogger(__name__)


providers = {
    'yandex': {
        'userinfo_endpoint': 'https://login.yandex.ru/info',
        'access_token_url': 'https://oauth.yandex.ru/token',
        'authorize_url': 'https://oauth.yandex.ru/authorize'
    }
}


class OAuthService:
    def __init__(self, oauth: OAuth, user_service: UserService):
        self.oauth = oauth
        self.user_service = user_service

        for provider, settings in providers.items():
            self.oauth.register(
                name=provider,
                **settings
            )

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
        client = self.oauth.create_client(provider)
        if not client:
            return None

        client.authorize_access_token()
        userinfo = client.userinfo()

        user = self.find_user(
            email=userinfo['default_email'], social_id=userinfo['id'], social_name=provider
        )

        if not user:
            user = self.user_service.registration_social(
                email=userinfo['default_email'], social_id=userinfo['id'], social_name=provider
            )

        return user

    def find_user(self, email: str, social_id: str, social_name: str):
        user = self.user_service.find_user(email)
        if not user:
            return None

        if self.user_service.find_social_user(social_id, social_name, user.id):
            return user

        return None


@lru_cache()
def get_oauth_service(oauth: OAuth, user_service: UserService) -> OAuthService:
    return OAuthService(oauth, user_service)
