from flask import url_for, jsonify
from flask_restx import Namespace, Resource, abort

from extensions.oauth import oauth

ns = Namespace('oauth', description='Внешняя авторизация')

parser = ns.parser()
parser.add_argument('provider', type=str, required=True, choices=("yandex",))


@ns.route('/login')
@ns.expect(parser)
class Login(Resource):
    def get(self):
        """Получаем ссылку для авторизации во внешнем сервисе"""
        provider = parser.parse_args().get('provider')
        client = oauth.create_client(provider)
        authorization_endpoint = url_for('api.oauth_authorize', provider=provider, _external=True, _scheme='https')
        # TODO: поискать нормальный способ получений урла
        return jsonify({
            'url': client.authorize_redirect(authorization_endpoint).location
        })


@ns.route('/authorize/<provider>')
class Authorize(Resource):
    def get(self, provider):
        client = oauth.create_client(provider)
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
