from flask import Flask
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from services.user import UserService, get_user_service
from config import Config


migrate = Migrate()
jwt = JWTManager()


def inject(binder):
    binder.bind(
        UserService,
        to=get_user_service()
    )


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    jwt.init_app(app)
    # FlaskInjector(app=app, modules=[inject])
    return app


def register_blueprints(app):
    from api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')


app = create_app(Config)
register_blueprints(app)


if __name__ == '__main__':
    app.run(debug=True)
