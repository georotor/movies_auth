from flask import Blueprint
from flask_restx import Api

from .user.routes import user

api_v1 = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    api_v1,
    version="1.0",
    title="Auth API",
    description="Модуль авторизации",
)

api.add_namespace(user, path='/user')
