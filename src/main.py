import logging

from flask import Flask, request
from flask_injector import FlaskInjector
from flask_migrate import Migrate

from config import Config
from db import db, ma, rd
from exts.jaeger import get_jaeger
from limiter import get_limiter
from exts.jwt import jwt
from exts.oauth import oauth
from models.role import Role, RoleSchema
from services.role import RoleService, get_role_service
from services.user import UserService, get_user_service
from services.oauth import OAuthService, get_oauth_service
from services.token import TokenService, get_token_service

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=Config.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

migrate = Migrate()
limiter = get_limiter()


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
    get_jaeger(app)

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


@app.before_request
def before_request():
    if not request.headers.get('X-Request-Id'):
        raise RuntimeError('Missing X-Request-Id')


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        debug=True
    )
