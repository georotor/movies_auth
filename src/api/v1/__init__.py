from flask import Blueprint
from flask_restx import Api

from .user.routes import user
from .roles.routes import roles
from .oauth.routes import ns as oauth

api_v1 = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    api_v1,
    version="1.0",
    title="Auth API",
    description="Модуль авторизации",
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'}
    }
)

api.add_namespace(user, path='/user')
api.add_namespace(roles, path='/roles')
api.add_namespace(oauth, path='/oauth')
