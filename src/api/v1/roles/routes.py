from http import HTTPStatus

from flask_injector import inject
from flask_restx import Namespace, Resource, abort

from .models import role, role_create, role_patch, role_assign, admin_required_model
from services.role import RoleService
from services.user import admin_required

roles = Namespace('roles', description='Управление ролями, доступно авторизованным администраторам')
roles.models[role.name] = role
roles.models[role_create.name] = role_create
roles.models[role_patch.name] = role_patch
roles.models[role_assign.name] = role_assign
roles.models[admin_required_model.name] = admin_required_model


class InjectResource(Resource):
    @inject
    def __init__(self, role_service: RoleService, **kwargs):
        self.role_service = role_service
        super().__init__(**kwargs)


@roles.route('/<uuid:role_id>')
@roles.doc(params={'role_id': 'Индификатор роли'}, security='Bearer')
@roles.response(int(HTTPStatus.UNAUTHORIZED), 'Authorization required')
@roles.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Incorrect authorization token')
@roles.response(int(HTTPStatus.FORBIDDEN), 'Access is denied')
class RolesUpdate(InjectResource):
    @roles.response(int(HTTPStatus.OK), 'Role was deleted')
    @roles.response(int(HTTPStatus.NOT_FOUND), 'Role does not exist')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
    @admin_required()
    def delete(self, role_id):
        """Удаление роли"""
        res = self.role_service.delete(role_id)
        match res:
            case None:
                abort(HTTPStatus.NOT_FOUND, 'Role does not exist')
            case True:
                return 'Role was deleted', HTTPStatus.OK
            case _:
                abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')

    @roles.expect(role_patch, validate=True)
    @roles.response(int(HTTPStatus.OK), 'Role successfully updated')
    @roles.response(int(HTTPStatus.CONFLICT), 'Role is already in use')
    @roles.response(int(HTTPStatus.NOT_FOUND), 'Role does not exist')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
    @admin_required()
    def patch(self, role_id):
        """Обновление данных роли"""
        res = self.role_service.update(role_id, roles.payload)
        match res:
            case None:
                abort(HTTPStatus.NOT_FOUND, 'Role does not exist')
            case False:
                abort(HTTPStatus.CONFLICT, 'Role is already in use')
            case True:
                return 'Role successfully updated', HTTPStatus.OK
            case _:
                abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')


@roles.route('')
@roles.doc(security='Bearer')
@roles.response(int(HTTPStatus.UNAUTHORIZED), 'Authorization required')
@roles.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Incorrect authorization token')
@roles.response(int(HTTPStatus.FORBIDDEN), 'Access is denied')
class Roles(InjectResource):
    @roles.marshal_list_with(role, code=int(HTTPStatus.OK))
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
    @admin_required()
    def get(self):
        """Список всех ролей"""
        return self.role_service.get_all(), HTTPStatus.OK

    @roles.expect(role_create, validate=True)
    @roles.marshal_with(role, code=int(HTTPStatus.CREATED))
    @roles.response(int(HTTPStatus.BAD_REQUEST), 'Input payload validation failed')
    @roles.response(int(HTTPStatus.CONFLICT), 'Role is already in use')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
    @admin_required()
    def post(self):
        """Создание новой роли"""
        new_role = self.role_service.create(**roles.payload)
        if new_role is None:
            abort(HTTPStatus.CONFLICT, 'Role is already in use')

        return new_role, HTTPStatus.CREATED


@roles.route('/assign')
@roles.doc(security='Bearer')
@roles.response(int(HTTPStatus.UNAUTHORIZED), 'Authorization required')
@roles.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Incorrect authorization token')
@roles.response(int(HTTPStatus.FORBIDDEN), 'Access is denied')
@roles.response(int(HTTPStatus.NOT_FOUND), 'Role or user does not exist')
@roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
class RolesAssign(InjectResource):
    @roles.expect(role_assign, validate=True)
    @roles.response(int(HTTPStatus.OK), 'User already has this role')
    @roles.response(int(HTTPStatus.BAD_REQUEST), 'Input payload validation failed')
    @admin_required()
    def get(self):
        """Проверка наличия роли у пользователя"""
        result = self.role_service.get_assigned_role(**roles.payload)
        if result is None:
            abort(HTTPStatus.NOT_FOUND, 'Role or user does not exist')
        if result is False:
            abort(HTTPStatus.NOT_FOUND, 'User does not has this role')

        return 'User already has this role', HTTPStatus.OK

    @roles.expect(role_assign, validate=True)
    @roles.response(int(HTTPStatus.OK), 'Role successfully added')
    @roles.response(int(HTTPStatus.BAD_REQUEST), 'Input payload validation failed')
    @admin_required()
    def post(self):
        """Добавление пользователю роли"""
        result = self.role_service.assign_role(**roles.payload)
        if result is None:
            abort(HTTPStatus.NOT_FOUND, 'Role or user does not exist')

        return 'Роль назначена', HTTPStatus.OK

    @roles.expect(role_assign, validate=True)
    @roles.response(int(HTTPStatus.OK), 'Role successfully deleted')
    @roles.response(int(HTTPStatus.BAD_REQUEST), 'Input payload validation failed')
    @admin_required()
    def delete(self):
        """Удаление роли у пользователя"""
        result = self.role_service.delete_assigned_role(**roles.payload)
        if result is None:
            abort(HTTPStatus.NOT_FOUND, 'Role or user does not exist.')

        return 'Role successfully deleted', HTTPStatus.OK
