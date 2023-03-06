from authlib.integrations.flask_client import OAuth

oauth = OAuth()

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
    },
    'mail': {
        'authorize_url': 'https://oauth.mail.ru/login',
        'access_token_url': 'https://oauth.mail.ru/token',
        'userinfo_endpoint': 'https://oauth.mail.ru/userinfo',
        'client_kwargs': {
            'scope': 'userinfo',
            'token_placement': 'uri',
        },
        'get_email': (lambda x: x['userinfo'].get('email')),
        'get_social_id': (lambda x: x['userinfo'].get('id'))
    },
    'google': {
        'access_token_url': 'https://oauth2.googleapis.com/token',
        'authorize_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'server_metadata_url': 'https://accounts.google.com/.well-known/openid-configuration',
        'client_kwargs': {
            'scope': 'openid email profile'
        },
        'get_email': (lambda x: x['userinfo'].get('email')),
        'get_social_id': (lambda x: x['userinfo'].get('sub'))
    }
}

for provider, settings in providers.items():
    oauth.register(
        name=provider,
        **settings
    )
