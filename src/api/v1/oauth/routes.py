from http import HTTPStatus

from flask import url_for, jsonify
from flask_injector import inject
from flask_restx import Namespace, Resource, abort

from .models import oauth_url
from services.oauth import OAuthService

ns = Namespace('oauth', description='Внешняя авторизация')
ns.models[oauth_url.name] = oauth_url

parser = ns.parser()
parser.add_argument('provider', type=str, required=True, choices=("yandex",))


class InjectResource(Resource):
    @inject
    def __init__(self, oauth_service: OAuthService, **kwargs):
        self.oauth_service = oauth_service
        super().__init__(**kwargs)


@ns.route('/login')
@ns.expect(parser)
class Login(InjectResource):
    @ns.marshal_with(oauth_url, code=int(HTTPStatus.OK))
    def get(self):
        """Получаем ссылку для авторизации во внешнем сервисе"""
        provider = parser.parse_args().get('provider')
        authorization_endpoint = url_for('api.oauth_authorize', provider=provider, _external=True, _scheme='https')

        url = self.oauth_service.get_auth_url(provider, authorization_endpoint)
        if not url:
            abort(404)

        return url


@ns.route('/authorize/<provider>')
class Authorize(InjectResource):
    def get(self, provider):
        client = self.oauth_service.oauth.create_client(provider)
        if not client:
            abort(404)

        # TODO: вынести всю эту бадягу в сервис
        # Получаем токен
        token = client.authorize_access_token()
        # Получаем данные пользователя
        user = client.userinfo()
        # Проверяем наличие пользователя в нашей базе, если нет то создаем
        # Пишем историю
        # Возвращаем новую пару наших JWT

        return jsonify(user)
