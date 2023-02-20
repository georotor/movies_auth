from functools import lru_cache
from uuid import UUID
from typing import Type

from flask_sqlalchemy import SQLAlchemy

from models.role import Role, RoleSchema
from models.user import User


class RoleService:
    def __init__(self, db: SQLAlchemy, model_role: Type[Role], model_role_schema: Type[RoleSchema]):
        self.db = db
        self.model_role = model_role
        self.model_role_schema = model_role_schema

    def _get_by_name(self, name: str) -> Role | None:
        """
        Поиск роли по наименованию.

        :param name: Название роли
        :return: None - если указанной роли не существует
                 или объект Role роли
        """
        return self.model_role.query.filter_by(name=name).one_or_none()

    def _get_by_id(self, role_id: UUID) -> Role | None:
        """
        Поиск роли по индификатору.

        :param role_id: Индификатор роли
        :return: None - если указанной роли не существует
                 или объект Role роли
        """
        return self.model_role.query.filter_by(id=role_id).one_or_none()

    def get_all(self) -> list[RoleSchema]:
        """
        Возвращает список ролей.
        """
        roles = self.model_role.query.all()
        return self.model_role_schema(many=True).dump(roles)

    def create(self, name: str, description: str = '') -> RoleSchema | None:
        """
        Создает новую роль.

        :param name: Название новой роли
        :param description: Описание новой роли
        :return: None - если указанной роли не существует
                 или объект RoleSchema новой роли
        """
        if self._get_by_name(name):
            return None

        role = self.model_role(name=name, description=description)
        self.db.session.add(role)
        self.db.session.commit()

        return self.model_role_schema().dump(role)

    def delete(self, role_id: UUID) -> bool | None:
        """
        Удаляет существующую роль.

        :param role_id: Индификатор роли
        :return: None - если указанной роли не существует
                 True - в случае успеха
        """
        role = self._get_by_id(role_id)
        if not role:
            return None

        self.db.session.delete(role)
        self.db.session.commit()

        return True

    def update(self, role_id: UUID, payload: dict) -> bool | None:
        """
        Обновляет существующую роль.

        :param role_id: Индификатор роли
        :param payload: Словарь с полями для обновления
        :return: None - если указанной роли не существует
                 False - если меняем название роли на уже существующее
                 True - в случае успеха
        """
        role = self._get_by_id(role_id)
        if not role:
            return None

        if 'name' in payload:
            other_role = self._get_by_name(payload['name'])
            if other_role and other_role.id != role.id:
                return False

        for key, value in payload.items():
            setattr(role, key, value)

        self.db.session.commit()

        return True

    def assign(self, user_id, role_id):
        role = self._get_by_id(role_id)
        if not role:
            return None

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return None

        user.roles.append(role)
        self.db.session.add(user)
        self.db.session.commit()

        return True



@lru_cache()
def get_role_service(
        db: SQLAlchemy,
        model_role: Type[Role],
        model_role_schema: Type[RoleSchema]
) -> RoleService:
    return RoleService(db, model_role, model_role_schema)
