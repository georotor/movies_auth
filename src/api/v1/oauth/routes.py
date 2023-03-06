from http import HTTPStatus

from flask import url_for, request
from flask_injector import inject
from flask_restx import Namespace, Resource, abort

from .models import oauth_url
from api.v1.user.models import tokens
from services.user import UserService
from services.oauth import OAuthService, OAuthError
from services.token import TokenService

ns = Namespace('oauth', description='Внешняя авторизация')
ns.models[oauth_url.name] = oauth_url
ns.models[tokens.name] = tokens

parser = ns.parser()
parser.add_argument('provider', type=str, required=True,
                    choices=("yandex", "vk", "mail", "google"))


class InjectResource(Resource):
    @inject
    def __init__(self, user_service: UserService, oauth_service: OAuthService, token_service: TokenService, **kwargs):
        self.user_service = user_service
        self.oauth_service = oauth_service
        self.token_service = token_service
        super().__init__(**kwargs)


@ns.route('/login/<provider>')
@ns.expect(parser)
class Login(InjectResource):
    @ns.marshal_with(oauth_url, code=int(HTTPStatus.OK))
    @ns.response(int(HTTPStatus.NOT_FOUND), 'Provider not found.')
    def get(self, provider):
        """Возвращает ссылку для авторизации во внешнем сервисе"""
        authorization_endpoint = url_for(
            'api.oauth_authorize', provider=provider, _external=True, _scheme='https')

        url = self.oauth_service.get_auth_url(provider, authorization_endpoint)
        if not url:
            abort(HTTPStatus.NOT_FOUND, 'Provider not found.')

        return url


@ns.route('/authorize/<provider>')
@ns.expect(parser)
class Authorize(InjectResource):
    @ns.marshal_with(tokens, code=int(HTTPStatus.OK))
    @ns.response(int(HTTPStatus.UNAUTHORIZED), 'Email required.')
    def get(self, provider):
        """Callback для авторизации через внешний сервис"""
        user = None
        try:
            user = self.oauth_service.authorize(provider)
        except OAuthError:
            abort(HTTPStatus.UNAUTHORIZED, 'Email required.')

        user_agent = request.user_agent.string
        self.user_service.remember_login(user.id, user_agent, action=f'login via {provider}')

        return self.token_service.create(user.id, fresh=True)
