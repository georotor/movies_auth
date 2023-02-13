from flask import Flask
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from config import Config
from models.role import Role
from services.user import UserService, get_user_service
from services.role import RoleService, get_role_service


migrate = Migrate()
jwt = JWTManager()


def configure(binder):
    binder.bind(UserService, to=get_user_service())
    binder.bind(RoleService, to=get_role_service(db, Role))


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
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
    app.run(debug=True)
