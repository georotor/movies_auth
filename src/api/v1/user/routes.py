from http import HTTPStatus
from flask_injector import inject
from flask_restx import Namespace, Resource, abort

from .models import user_create, token, tokens
from services.user import UserService

user = Namespace('user', description='Авторизация пользователей')
user.models[user_create.name] = user_create
user.models[token.name] = token
user.models[tokens.name] = tokens


@user.route('/signup')
class SignUp(Resource):
    @inject
    def __init__(self, user_service: UserService, **kwargs):
        self.user_service = user_service
        super().__init__(**kwargs)

    # Валидируем входные данные
    @user.expect(user_create, validate=True)
    # Валидируем выходные данные
    @user.marshal_with(tokens, code=int(HTTPStatus.CREATED))
    # Добавляем в сваггер варианты ответа
    @user.response(int(HTTPStatus.BAD_REQUEST), 'Input payload validation failed.')
    @user.response(int(HTTPStatus.CONFLICT), 'Email is already registered.')
    @user.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.')
    def post(self):
        tokens_new = self.user_service.create(
            email=user.payload['email'],
            password=user.payload['password']
        )
        if tokens_new is None:
            abort(HTTPStatus.CONFLICT, 'Email is already registered.')

        return tokens_new, HTTPStatus.CREATED

