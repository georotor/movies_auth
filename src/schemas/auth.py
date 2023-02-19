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
    """Схема для регистрации пользователя с дополнительной валидацией полей.
    Возвращает модель пользователя.

    """
    email = fields.String(required=True)
    password = fields.String(required=True)

    @validates("email")
    def validates_email(self, value):
        if not re.match(r"^\S+@\S+\.\S+$", value):
            raise ValidationError("Please, enter valid email address")

    @validates("password")
    def validates_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters")

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)
