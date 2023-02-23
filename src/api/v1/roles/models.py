from flask_restx import Model, SchemaModel, fields

role = Model(
    'Role',
    {
        'id': fields.String(required=True),
        'name': fields.String(required=True, max_length=80),
        'description': fields.String(max_length=255)
    }
)

role_create = Model(
    'RoleCreate',
    {
        'name': fields.String(required=True, max_length=80),
        'description': fields.String(max_length=255)
    }
)

role_assign = Model(
    'RoleAssign',
    {
        'user_id': fields.String(required=True),
        'role_id': fields.String(required=True),
    }
)

admin_required_model = Model(
    "AdminRequired", {
        "msg": fields.String(required=True)
    }
)

role_patch = SchemaModel(
    'RolePatch',
    {
        'type': 'object',
        'properties': {
            'name': {'type': 'string', 'maxLength': 80},
            'description': {'type': 'string', 'maxLength': 255},
        },
        'anyOf': [{'required': ['name']}, {'required': ['description']}]
    }
)
