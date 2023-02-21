import re

from marshmallow import Schema, ValidationError, fields, post_load, validates

from models.user import User


class LoginSchema(Schema):
    """Схема для аутентификации пользователя. Возвращает модель пользователя
    либо поднимает ошибку.

    """
    email = fields.String(required=True)
    password = fields.String(required=True)

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)


class RegistrationSchema(Schema):
    """Схема для регистрации пользователя. Возвращает модель пользователя.

    Валидация полей отдана restx, данные проверяются на уровне api.
    При необходимости ее можно реализовать в схеме вот так:

    @validates("password")
    def validates_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters")

    """
    email = fields.String(required=True)
    password = fields.String(required=True)

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)


class UpdateUserSchema(Schema):
    """Схема для обновления данных. Возвращает модель пользователя.

    Валидация полей отдана restx, данные проверяются на уровне api.
    При необходимости ее можно реализовать в схеме вот так:

    @validates("password")
    def validates_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters")

    """
    id = fields.UUID(required=True)
    email = fields.String(required=False)
    password = fields.String(required=False)

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)
