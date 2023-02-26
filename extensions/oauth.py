from authlib.integrations.flask_client import OAuth

oauth = OAuth()

oauth.register(
    name='yandex',
    userinfo_endpoint='https://login.yandex.ru/info'
)
