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
    'ok': {
        'authorize_url': 'https://connect.ok.ru/oauth/authorize',
        'access_token_url': 'https://api.ok.ru/oauth/token.do',
        'client_kwargs': {
            'scope': 'VALUABLE_ACCESS;LONG_ACCESS_TOKEN;GET_EMAIL'
        },
        'get_email': (lambda x: x['userinfo'].get('email')),
        'get_social_id': (lambda x: x['userinfo'].get('id'))
    },
}

for provider, settings in providers.items():
    oauth.register(
        name=provider,
        **settings
    )
