import logging

from flask import Flask
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import Config
from db import db, ma, rd
from limiter import get_limiter
from exts.oauth import oauth
from models.role import Role, RoleSchema
from models.user import User
from services.role import RoleService, get_role_service
from services.user import UserService, get_user_service
from services.oauth import OAuthService, get_oauth_service
from services.token import TokenService, get_token_service

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=Config.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

migrate = Migrate()
jwt = JWTManager()
limiter = get_limiter()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """Callback, используется flask-jwt-extended для проверки статуса токена.
    https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking/#redis

    """
    key = jwt_payload["jti"]
    token_in_redis = rd.get(key)
    if token_in_redis:
        logger.info('Токен (type:{}) пользователя <{}> в стоп листе'.format(jwt_payload['type'], jwt_payload['sub']))
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
    binder.bind(OAuthService, to=get_oauth_service(oauth, get_user_service()))
    binder.bind(TokenService, to=get_token_service())


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    ma.init_app(app)
    rd.init_app(app)

    oauth.init_app(app)

    limiter.init_app(app)

    migrate.init_app(app, db)

    jwt.init_app(app)

    return app


def register_blueprints(app):
    from api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    from shell import shell
    app.register_blueprint(shell, cli_group=None)

    FlaskInjector(app=app, modules=[configure])


app = create_app(Config)
register_blueprints(app)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        debug=True
    )
