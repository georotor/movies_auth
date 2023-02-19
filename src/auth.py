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

    access_token, refresh_token = token_service.create(
        user_id, user_agent, fresh=True
    )

    return jsonify(
        access_token=access_token, refresh_token=refresh_token
    ), HTTPStatus.CREATED


@auth.route('/login', methods=['POST'])
def login():

    user_id = auth_service.login(request.json)

    user_host = request.remote_addr  # todo: добавить в UserHistory
    user_agent = request.user_agent.string
    auth_service.remember_login(user_id, user_agent)

    access_token, refresh_token = token_service.create(user_id, user_agent)

    return jsonify(
        access_token=access_token, refresh_token=refresh_token
    ), HTTPStatus.OK


@auth.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    """Есть несколько разных способов отзывать токены при выходе пользователя.
    В документации https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking/#redis
    сказано, что ответственность за генерацию запросов на отзыв и access и
    refresh токенов обычно ложится на frontend. Со стороны backend достаточно
    предоставить один универсальный метод @jwt_required(verify_type=False), с
    помощью которого можно отозвать любой токен.

    Важный момент! Отзывать только access токен бессмысленно - пока "жив"
    refresh токен пользователь сможет запросить новый.

    """
    user_agent = request.headers['user_agent']
    ex_token_type = token_service.delete(user_agent)
    return jsonify(msg="{} token successfully revoked".format(ex_token_type))


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Получение новой пары токенов на основании действующего refresh токена.
    Перед этим убеждаемся, что refresh токен и user_agent не менялись.

    """
    user_agent = request.headers['user_agent']

    if not token_service.check_owner(user_agent):
        return jsonify(
            msg='Token does not belong to this user'
        ), HTTPStatus.CONFLICT

    access_token, refresh_token = token_service.refresh(user_agent)

    return jsonify(
        access_token=access_token, refresh_token=refresh_token
    ), HTTPStatus.OK


@auth.route("/protected")
@jwt_required()
def protected():
    return make_response({'msg': 'OK'}, HTTPStatus.OK)
