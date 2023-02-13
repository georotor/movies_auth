from http import HTTPStatus
from flask_injector import inject
from flask_restx import Namespace, Resource, abort

from .models import role, role_create
from services.role import RoleService

roles = Namespace('roles', description='Управление ролями')
roles.models[role.name] = role
roles.models[role_create.name] = role_create


@roles.route('/')
class RoleCreate(Resource):
    @inject
    def __init__(self, role_service: RoleService, **kwargs):
        self.role_service = role_service
        super().__init__(**kwargs)

    @roles.expect(role_create, validate=True)
    @roles.marshal_with(role, code=int(HTTPStatus.CREATED))
    @roles.response(int(HTTPStatus.BAD_REQUEST), 'Ошибка проверки входных данных.')
    @roles.response(int(HTTPStatus.CONFLICT), 'Роль с таким названием уже есть.')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутрення ошибка сервера.')
    def post(self):
        new_role = self.role_service.create(**roles.payload)
        if new_role is None:
            abort(HTTPStatus.CONFLICT, 'Роль с таким названием уже есть.')

        return new_role, HTTPStatus.CREATED



