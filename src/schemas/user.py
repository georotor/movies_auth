from marshmallow import post_load
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
