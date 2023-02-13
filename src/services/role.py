from functools import lru_cache
from typing import Type

from flask_sqlalchemy import SQLAlchemy

from models.role import Role, RoleSchema


class RoleService:
    def __init__(self, db: SQLAlchemy, model_role: Type[Role], model_role_schema: Type[RoleSchema]):
        self.db = db
        self.model_role = model_role
        self.model_role_schema = model_role_schema

    def find_by_name(self, name):
        return self.model_role.query.filter_by(name=name).one_or_none()

    def create(self, name: str, description: str):

        if self.find_by_name(name):
            return None

        role = self.model_role(name=name, description=description)
        self.db.session.add(role)
        self.db.session.commit()

        return self.model_role_schema().dump(role)


@lru_cache()
def get_role_service(
        db: SQLAlchemy,
        model_role: Type[Role],
        model_role_schema: Type[RoleSchema]
) -> RoleService:
    return RoleService(db, model_role, model_role_schema)
