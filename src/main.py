from datetime import timedelta

from flask import Flask
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager

from api.v1 import api_v1
from db import db, init_db
from services.user import UserService, get_user_service


def configure(binder):
    binder.bind(
        UserService,
        to=get_user_service()
    )


if __name__ == '__main__':
    app = Flask(__name__)

    init_db(app)
    app.app_context().push()
    db.create_all()

    app.config["RESTX_MASK_SWAGGER"] = False

    app.config["JWT_TOKEN_LOCATION"] = 'headers'
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager(app)

    app.register_blueprint(api_v1, url_prefix="/api/v1")
    FlaskInjector(app=app, modules=[configure])
    app.run(debug=True)
