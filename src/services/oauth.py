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


@lru_cache()
def get_oauth_service(oauth: OAuth) -> OAuthService:
    return OAuthService(oauth)
