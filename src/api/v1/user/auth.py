from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required

from services.auth import AuthError, AuthService
from services.token import TokenService

auth = Blueprint("auth", __name__)

auth_service = AuthService()
token_service = TokenService()


@auth.route('/register', methods=['POST'])
def create_new_user():
    """Регистрация: создание нового пользователя и возврат пары токенов.
    Данные можно или получать в json или брать из заголовка http request.

    На данный момент используется request.json, но можно легко переделать:

    email = request.values.get('email', None)
    password = request.values.get('password', None)

    """
    try:
        user_id = auth_service.registration(request.json)
    except AuthError as e:
        return jsonify({'msg': str(e)}), HTTPStatus.CONFLICT

    user_host = request.remote_addr  # todo: добавить в UserHistory
    user_agent = request.user_agent.string
    auth_service.remember_login(user_id, user_agent, action='registration')

    access_token, refresh_token = token_service.create(user_id, fresh=True)

    expire = token_service.expired_at()
    return jsonify(
        access_token=access_token, refresh_token=refresh_token, expire=expire,
    ), HTTPStatus.CREATED


@auth.route('/login', methods=['POST'])
def login():

    user_id = auth_service.login(request.json)

    user_host = request.remote_addr  # todo: добавить в UserHistory
    user_agent = request.user_agent.string
    auth_service.remember_login(user_id, user_agent)

    access_token, refresh_token = token_service.create(user_id)
    expire = token_service.expired_at()
    return jsonify(
        access_token=access_token, refresh_token=refresh_token, expire=expire,
    ), HTTPStatus.OK


@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    """Есть несколько разных способов отзывать токены при выходе пользователя.
    В документации https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking/#redis
    сказано, что ответственность за генерацию запросов на отзыв и access и
    refresh токенов обычно ложится на frontend. Со стороны backend достаточно
    предоставить один универсальный метод @jwt_required(verify_type=False), с
    помощью которого можно отозвать любой токен.

    В нашей реализации мы оставляем всю логику в backend. Это гарантирует, что
    будут отозваны оба токена разом.

    """
    token_service.delete()
    return jsonify(msg="Tokens successfully revoked")


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Получение новой пары токенов на основании действующего refresh токена.

    """
    access_token, refresh_token = token_service.refresh()
    expire = token_service.expired_at()

    return jsonify(
        access_token=access_token, refresh_token=refresh_token, expire=expire,
    ), HTTPStatus.OK


@auth.route("/protected")
@jwt_required()
def protected():
    return make_response({'msg': 'OK'}, HTTPStatus.OK)
