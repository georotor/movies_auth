""" Модели для валидации входных и выходных данных """

from flask_restx import Model, SchemaModel, fields

EMAIL_PATTERN = r'^([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$'

user_create = Model(
    'UserCreate',
    {
        'email': fields.String(
            required=True,
            pattern=EMAIL_PATTERN,
        ),
        'password': fields.String(required=True, min_length=8)
    }
)

user_update = SchemaModel(
    'UserUpdate',
    {
        'type': 'object',
        'properties': {
            'email': {'type': 'string', 'pattern': EMAIL_PATTERN},
            'password': {'type': 'string', 'minLength': 8},
        },
        'anyOf': [{'required': ['email']}, {'required': ['password']}]
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

user_history_request = Model(
    'UserCreate',
    {
        'page_number': fields.Integer(required=True, min=1),
        'page_size': fields.Integer(default=1),
    }
)

user_history = Model(
    'UserHistory',
    {
        'user_agent': fields.String,
        'action': fields.String,
        'created': fields.DateTime,
    }
)