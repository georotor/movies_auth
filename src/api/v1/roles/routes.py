from http import HTTPStatus
from flask_injector import inject
from flask_restx import Namespace, Resource, abort

from .models import role, role_create, role_patch
from services.role import RoleService

roles = Namespace('roles', description='Управление ролями')
roles.models[role.name] = role
roles.models[role_create.name] = role_create
roles.models[role_patch.name] = role_patch


@roles.route('/<uuid:role_id>')
@roles.doc(params={'role_id': 'Индификатор роли'})
class RolesUpdate(Resource):
    @inject
    def __init__(self, role_service: RoleService, **kwargs):
        self.role_service = role_service
        super().__init__(**kwargs)

    @roles.response(int(HTTPStatus.OK), 'Роль удалена.')
    @roles.response(int(HTTPStatus.NOT_FOUND), 'Роль не существует.')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера.')
    def delete(self, role_id):
        res = self.role_service.delete(role_id)
        match res:
            case None:
                abort(HTTPStatus.NOT_FOUND, 'Роль не существует.')
            case True:
                return
            case _:
                abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'Внутренняя ошибка сервера.')

    @roles.expect(role_patch, validate=True)
    @roles.response(int(HTTPStatus.OK), 'Роль обновлена.')
    @roles.response(int(HTTPStatus.CONFLICT), 'Роль с таким названием уже существует.')
    @roles.response(int(HTTPStatus.NOT_FOUND), 'Роль не существует.')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера.')
    def patch(self, role_id):
        res = self.role_service.update(role_id, roles.payload)
        match res:
            case None:
                abort(HTTPStatus.NOT_FOUND, 'Роль не существует.')
            case False:
                abort(HTTPStatus.CONFLICT, 'Роль с таким названием уже существует.')
            case True:
                return
            case _:
                abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'Внутренняя ошибка сервера.')


@roles.route('')
class Roles(Resource):
    @inject
    def __init__(self, role_service: RoleService, **kwargs):
        self.role_service = role_service
        super().__init__(**kwargs)

    @roles.marshal_list_with(role, code=int(HTTPStatus.OK))
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера.')
    def get(self):
        return self.role_service.get_all()

    @roles.expect(role_create, validate=True)
    @roles.marshal_with(role, code=int(HTTPStatus.CREATED))
    @roles.response(int(HTTPStatus.BAD_REQUEST), 'Ошибка проверки входных данных.')
    @roles.response(int(HTTPStatus.CONFLICT), 'Роль с таким названием уже есть.')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера.')
    def post(self):
        new_role = self.role_service.create(**roles.payload)
        if new_role is None:
            abort(HTTPStatus.CONFLICT, 'Роль с таким названием уже есть.')

        return new_role, HTTPStatus.CREATED



