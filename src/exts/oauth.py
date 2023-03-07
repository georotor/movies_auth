from authlib.integrations.flask_client import OAuth

from config import config


oauth = OAuth()
"""
Вынес все параметры с URL и scope в конфиг, чтобы их можно было "перегрузить" через переменные окружения.
Но не считаю это верным решением, т.к. вероятность того что сервис изменит какой-нибудь URL ничуть не больше 
того что он изменит названием или местонахождение требуемого нам параметра, конечно и это можно решить
путем внедрения каких-нибудь шаблонов, но это кажется слишком избыточным :)
Возможно есть еще какие то аргументы, т.к. авторы authlib пишут в своей документации:
We suggest that you keep ONLY {name}_CLIENT_ID and {name}_CLIENT_SECRET in your Flask application configuration.
"""
providers = {
    'yandex': {
        'get_email': (lambda x: x['userinfo'].get('default_email')),
        'get_social_id': (lambda x: x['userinfo'].get('id'))
    },
    'vk': {
        'get_email': (lambda x: x['token'].get('email')),
        'get_social_id': (lambda x: x['token'].get('user_id'))
    },
    'mail': {
        'get_email': (lambda x: x['userinfo'].get('email')),
        'get_social_id': (lambda x: x['userinfo'].get('id'))
    },
    'google': {
        'get_email': (lambda x: x['userinfo'].get('email')),
        'get_social_id': (lambda x: x['userinfo'].get('sub'))
    }
}

for provider, settings in providers.items():
    for key in filter(lambda n: n.startswith(f'{provider.upper()}_'),  config.__fields__):
        name = key[len(provider)+1:].lower()
        settings[name] = getattr(config, key)

    oauth.register(
        name=provider,
        **settings
    )
