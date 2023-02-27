import logging
from functools import lru_cache

from authlib.integrations.flask_client import OAuth
from services.user import UserService

logger = logging.getLogger(__name__)


class OAuthError(Exception):
    """Исключение для ошибок при аутентификации."""


providers = {
    'yandex': {
        'userinfo_endpoint': 'https://login.yandex.ru/info',
        'access_token_url': 'https://oauth.yandex.ru/token',
        'authorize_url': 'https://oauth.yandex.ru/authorize',
        'get_email': (lambda x: x['userinfo'].get('default_email')),
        'get_social_id': (lambda x: x['userinfo'].get('id'))
    },
    'vk': {
        'api_base_url': 'https://api.vk.com/method/',
        'access_token_url': 'https://oauth.vk.com/access_token',
        'authorize_url': 'https://oauth.vk.com/authorize',
        'userinfo_endpoint': 'users.get?fields=sex,bdate,screen_name&v=5.131',
        'client_kwargs': {
            'token_placement': 'uri',
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'email'
        },
        'get_email': (lambda x: x['token'].get('email')),
        'get_social_id': (lambda x: x['token'].get('user_id'))
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

        user = self.find_user(email=email, social_id=social_id, social_name=provider)

        if not user:
            user = self.user_service.registration_social(
                email=email, social_id=social_id, social_name=provider
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
