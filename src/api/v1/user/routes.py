"""Ручки для работы с пользователем и его токенами.
Регистрация, аутентификация, выход, перевыпуск токенов.

Используются следующие декораторы restx:

Валидация входных данных: @user.expect
Валидация выходных данных: @user.marshal_with
Варианты ответа для swagger: @user.response

"""

from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, abort

from services.auth import AuthError, AuthService
from services.token import TokenService, TokenError

from .models import token, tokens, user_create

auth_service = AuthService()
token_service = TokenService()

user = Namespace('user', description='Авторизация пользователей')
user.models[user_create.name] = user_create
user.models[token.name] = token
user.models[tokens.name] = tokens


@user.route('/signup')
class SignUp(Resource):
    @user.expect(user_create, validate=True)
    @user.marshal_with(tokens, code=int(HTTPStatus.CREATED))
    @user.response(
        int(HTTPStatus.BAD_REQUEST), 'Input payload validation failed.'
    )
    @user.response(int(HTTPStatus.CONFLICT), 'Email is already registered.')
    @user.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.'
    )
    def post(self):
        """Регистрация пользователя в дополнительной валидацией данных. После
        регистрации пользователь сразу считается аутентифицированным.

        """
        try:
            user_id = auth_service.registration(request.json)
        except AuthError:
            abort(HTTPStatus.CONFLICT, 'Email is already registered.')
            return

        user_agent = request.user_agent.string
        auth_service.remember_login(user_id, user_agent, action='registration')

        access_token, refresh_token = token_service.create(user_id, fresh=True)

        tokens_ = {
            'access': {
                'token': access_token,
                'expired': token_service.expired_at(access_token)
            },
            'refresh': {
                'token': refresh_token,
                'expired': token_service.expired_at(refresh_token)
            },
        }

        return tokens_


@user.route('/login')
class LogIn(Resource):
    @user.expect(user_create, validate=True)
    @user.marshal_with(tokens, code=int(HTTPStatus.CREATED))
    @user.response(
        int(HTTPStatus.BAD_REQUEST), 'Input payload validation failed.'
    )
    @user.response(
        int(HTTPStatus.UNAUTHORIZED), 'Invalid username or password.'
    )
    @user.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.'
    )
    def post(self):
        """Аутентификация пользователя в дополнительной валидацией данных.

        """
        try:
            user_id = auth_service.login(request.json)
        except AuthError:
            abort(HTTPStatus.UNAUTHORIZED, 'Invalid username or password.')
            return

        user_agent = request.user_agent.string
        auth_service.remember_login(user_id, user_agent)

        access_token, refresh_token = token_service.create(user_id, fresh=True)

        tokens_ = {
            'access': {
                'token': access_token,
                'expired': token_service.expired_at(access_token)
            },
            'refresh': {
                'token': refresh_token,
                'expired': token_service.expired_at(refresh_token)
            },
        }

        return tokens_


@user.route('/logout')
class LogOut(Resource):
    @user.response(
        int(HTTPStatus.OK), 'Tokens successfully revoked.'
    )
    @user.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.'
    )
    @jwt_required()
    def delete(self):
        """Отзываем access токен и связанный с ним refresh токен. Это
        гарантирует, что пользователь не сможет их перевыпустить без повторной
        аутентификации.

        """
        token_service.delete()
        return HTTPStatus.OK, 'Tokens successfully revoked.'


@user.route('/refresh')
class Refresh(Resource):
    @user.marshal_with(tokens, code=int(HTTPStatus.CREATED))
    @user.response(
        int(HTTPStatus.UNAUTHORIZED), 'Token authentication failed.'
    )
    @user.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.'
    )
    @jwt_required(refresh=True)
    def post(self):
        """Получение новой пары токенов на основании действующего refresh
        токена.

        """
        try:
            access_token, refresh_token = token_service.refresh()
        except TokenError:
            abort(HTTPStatus.UNAUTHORIZED, 'Token authentication failed.')
            return

        tokens_ = {
            'access': {
                'token': access_token,
                'expired': token_service.expired_at(access_token)
            },
            'refresh': {
                'token': refresh_token,
                'expired': token_service.expired_at(refresh_token)
            },
        }

        return tokens_

