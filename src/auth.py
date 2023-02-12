"""
Вопрос номер один - где хранятся активные токены? Редис? Куки? Psql?
Вопрос номер два - как должен выглядеть класс юзера из сервисов?

"""


from http import HTTPStatus

from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jti,
    get_jwt_identity,
    JWTManager,
)

from services.user import UserService

auth = Blueprint("auth", __name__)
jwt = JWTManager()

# sess = scoped_session(sessionmaker())  # UserSchema().load(jsn, session=sess)


@auth.route('/register', methods=['POST'])
def create_new_user():
    username = request.values.get('username', None)
    password = request.values.get('password', None)

    user_host = request.remote_addr
    user_agent = request.user_agent

    if not username or not password:
        msg = jsonify({'msg': 'Missing mandatory parameters.'})
        return msg, HTTPStatus.BAD_REQUEST

    user = UserService()
    user.create(username, password)

    if not user.id:  # todo: костыль, нужно менять метод в UserService
        msg = jsonify({'msg': 'User already exists.'})
        return msg, HTTPStatus.CONFLICT

    user.log(user_host, user_agent)

    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)

    msg = jsonify(
        {'msg': 'User successfully created.',
         'access_token': access_token,
         'refresh_token': refresh_token}
    )
    return make_response(msg, HTTPStatus.CREATED)


@auth.route('/login', methods=['POST'])
def login():
    username = request.authorization.username
    password = request.authorization.password

    if not username or not password:
        msg = jsonify({'msg': 'Authentication faild.'})
        return make_response(msg, HTTPStatus.UNAUTHORIZED)

    user = UserService()
    if user.login(username, password) is None:
        msg = jsonify({'msg': 'Authentication faild.'})
        return make_response(msg, HTTPStatus.UNAUTHORIZED)

    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)
    # ключ для редиса - jti, он же unique identifier of an encoded JWT
    redis_key = get_jti(refresh_token)  # todo: добавить запись в Redis

    msg = jsonify(
        {'msg': 'Authentication successfully completed.',
         'access_token': access_token,
         'refresh_token': refresh_token}
    )
    return make_response(msg, HTTPStatus.OK)


@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    # https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking/
    # ключ для редиса - jti, он же unique identifier of an encoded JWT
    redis_key = get_jwt()["jti"]  # todo: удалить запись из Redis
    msg = jsonify({'msg': 'Logout successfully completed.'})
    return make_response(msg, HTTPStatus.OK)


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    # https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
    exp_timestamp = get_jwt()["exp"]
    now = datetime.now()
    target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
    if target_timestamp > exp_timestamp:
        access_token = create_access_token(identity=get_jwt_identity())

