from marshmallow import post_load, Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models.user import User, UserHistory


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        load_only = ("password",)
        include_relationships = True
        fields = ('email', 'password', 'is_admin')


class UserHistorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserHistory
        fields = ('user_id', 'user_agent', 'action', 'created')
        load_only = ("user_id",)

    @post_load
    def create_user_history(self, data, **kwargs):
        return UserHistory(**data)


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
