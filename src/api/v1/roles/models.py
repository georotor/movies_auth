from flask_restx import Model, fields

role = Model(
    'Role',
    {
        'id': fields.String(required=True),
        'name': fields.String(required=True),
        'description': fields.String()
    }
)

role_create = Model(
    'RoleCreate',
    {
        'name': fields.String(required=True),
        'description': fields.String()
    }
)