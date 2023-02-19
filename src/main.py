from flask import Flask, request
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import Config
from db import db, ma, rd
from models.role import Role, RoleSchema
from models.user import User
from services.role import RoleService, get_role_service
from services.user import UserService, get_user_service

migrate = Migrate()
jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """Callback, используется flask-jwt-extended для проверки статуса токена.
    https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking/#redis

    """
    user_agent = request.headers['user_agent']
    jti = jwt_payload["jti"]
    key = ':'.join((jti, user_agent))
    token_in_redis = rd.get(key)
    return token_in_redis is not None


@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    """Callback, используется при создании токена с дополнительными данными.
    https://flask-jwt-extended.readthedocs.io/en/latest/add_custom_data_claims/

    В данном случае используем его для хранения флага is_admin, теоретически
    сюда можно положить список всех ролей пользователя.

    """
    user = User.query.filter_by(id=identity).one_or_none()
    return {'is_admin': user.is_admin}


def configure(binder):
    binder.bind(UserService, to=get_user_service())
    binder.bind(RoleService, to=get_role_service(db, Role, RoleSchema))


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    ma.init_app(app)

    migrate.init_app(app, db)

    jwt.init_app(app)

    return app


def register_blueprints(app):
    from api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    from auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from shell import shell
    app.register_blueprint(shell, cli_group=None)

    FlaskInjector(app=app, modules=[configure])


app = create_app(Config)
register_blueprints(app)


if __name__ == '__main__':
    app.run(debug=True)
