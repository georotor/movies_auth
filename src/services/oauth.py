import logging
from functools import lru_cache

from authlib.integrations.flask_client import OAuth

logger = logging.getLogger(__name__)


providers = {
    'yandex': {
        'userinfo_endpoint': 'https://login.yandex.ru/info',
        'access_token_url': 'https://oauth.yandex.ru/token',
        'authorize_url': 'https://oauth.yandex.ru/authorize'
    }
}


class OAuthService:
    def __init__(self, oauth: OAuth):
        self.oauth = oauth

        for provider, settings in providers.items():
            self.oauth.register(
                name=provider,
                **settings
            )

    def get_auth_url(self, provider, authorization_endpoint) -> tuple | None:
        client = self.oauth.create_client(provider)
        if not client:
            return None

        rv = client.create_authorization_url(authorization_endpoint)
        client.save_authorize_data(redirect_uri=authorization_endpoint, **rv)

        return rv


@lru_cache()
def get_oauth_service(oauth: OAuth) -> OAuthService:
    return OAuthService(oauth)
