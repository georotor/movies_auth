from flask_restx import Model, SchemaModel, fields

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

role_patch = SchemaModel(
    'RolePatch',
    {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
        },
        'anyOf': [{'required': ['name']}, {'required': ['description']}]
    }
)