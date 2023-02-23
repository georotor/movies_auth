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
@roles.response(int(HTTPStatus.UNAUTHORIZED), 'Необходима авторизация')
@roles.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Некорректный токен авторизации')
@roles.response(int(HTTPStatus.FORBIDDEN), 'Доступ запрещен')
class RolesUpdate(InjectResource):
    @roles.response(int(HTTPStatus.OK), 'Роль удалена')
    @roles.response(int(HTTPStatus.NOT_FOUND), 'Роль не существует')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера')
    @admin_required()
    def delete(self, role_id):
        """Удаление роли"""
        res = self.role_service.delete(role_id)
        match res:
            case None:
                abort(HTTPStatus.NOT_FOUND, 'Роль не существует')
            case True:
                return 'Роль удалена', HTTPStatus.OK
            case _:
                abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'Внутренняя ошибка сервера')

    @roles.expect(role_patch, validate=True)
    @roles.response(int(HTTPStatus.OK), 'Роль обновлена')
    @roles.response(int(HTTPStatus.CONFLICT), 'Роль с таким названием уже существует')
    @roles.response(int(HTTPStatus.NOT_FOUND), 'Роль не существует')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера')
    @admin_required()
    def patch(self, role_id):
        """Обновление данных роли"""
        res = self.role_service.update(role_id, roles.payload)
        match res:
            case None:
                abort(HTTPStatus.NOT_FOUND, 'Роль не существует')
            case False:
                abort(HTTPStatus.CONFLICT, 'Роль с таким названием уже существует')
            case True:
                return 'Роль обновлена', HTTPStatus.OK
            case _:
                abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'Внутренняя ошибка сервера')


@roles.route('')
@roles.doc(security='Bearer')
@roles.response(int(HTTPStatus.UNAUTHORIZED), 'Необходима авторизация')
@roles.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Некорректный токен авторизации')
@roles.response(int(HTTPStatus.FORBIDDEN), 'Доступ запрещен')
class Roles(InjectResource):
    @roles.marshal_list_with(role, code=int(HTTPStatus.OK))
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера')
    @admin_required()
    def get(self):
        """Список всех ролей"""
        return self.role_service.get_all(), HTTPStatus.OK

    @roles.expect(role_create, validate=True)
    @roles.marshal_with(role, code=int(HTTPStatus.CREATED))
    @roles.response(int(HTTPStatus.BAD_REQUEST), 'Ошибка проверки входных данных')
    @roles.response(int(HTTPStatus.CONFLICT), 'Роль с таким названием уже есть')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера')
    @admin_required()
    def post(self):
        """Создание новой роли"""
        new_role = self.role_service.create(**roles.payload)
        if new_role is None:
            abort(HTTPStatus.CONFLICT, 'Роль с таким названием уже есть')

        return new_role, HTTPStatus.CREATED


@roles.route('/assign')
@roles.doc(security='Bearer')
@roles.response(int(HTTPStatus.UNAUTHORIZED), 'Необходима авторизация')
@roles.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Некорректный токен авторизации')
@roles.response(int(HTTPStatus.FORBIDDEN), 'Доступ запрещен')
class RolesAssign(InjectResource):
    @roles.response(int(HTTPStatus.OK), 'У пользователя есть такая роль')
    @roles.response(int(HTTPStatus.BAD_REQUEST), 'Ошибка проверки входных данных')
    @roles.response(int(HTTPStatus.NOT_FOUND), 'Роль или пользователь не существует')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера')
    @admin_required()
    def get(self):
        """Проверка наличия роли у пользователя"""
        result = self.role_service.get_assigned_role(**roles.payload)
        if result is None:
            abort(HTTPStatus.NOT_FOUND, 'Роль или пользователь не существует')
        if result is False:
            abort(HTTPStatus.NOT_FOUND, 'Пользователь не имеет такой роли')

        return 'У пользователя есть такая роль', HTTPStatus.OK

    @roles.expect(role_assign, validate=True)
    @roles.response(int(HTTPStatus.OK), 'Роль назначена')
    @roles.response(int(HTTPStatus.BAD_REQUEST), 'Ошибка проверки входных данных')
    @roles.response(int(HTTPStatus.NOT_FOUND), 'Роль или пользователь не существует')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера')
    @admin_required()
    def post(self):
        """Добавление пользователю роли"""
        result = self.role_service.assign_role(**roles.payload)
        if result is None:
            abort(HTTPStatus.NOT_FOUND, 'Роль или пользователь не существует')

        return 'Роль назначена', HTTPStatus.OK

    @roles.response(int(HTTPStatus.OK), 'Роль для данного пользователя удалена')
    @roles.response(int(HTTPStatus.BAD_REQUEST), 'Ошибка проверки входных данных')
    @roles.response(int(HTTPStatus.NOT_FOUND), 'Роль или пользователь не существует')
    @roles.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Внутренняя ошибка сервера')
    @admin_required()
    def delete(self):
        """Удаление роли у пользователя"""
        result = self.role_service.delete_assigned_role(**roles.payload)
        if result is None:
            abort(HTTPStatus.NOT_FOUND, 'Роль или пользователь не существует.')

        return 'Роль для данного пользователя удалена', HTTPStatus.OK
