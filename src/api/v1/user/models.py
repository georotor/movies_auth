""" Модели для валидации входных и выходных данных """

from flask_restx import Model, fields

user_create = Model(
    'UserCreate',
    {
        'email': fields.String(required=True,
                               pattern=r'^([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$'),
        'password': fields.String(required=True, min_length=8)
    }
)

token = Model(
    'Token',
    {
        'token': fields.String,
        'expired': fields.DateTime
    }
)

tokens = Model(
    'Tokens',
    {
        'access': fields.Nested(token),
        'refresh': fields.Nested(token)
    }
)
