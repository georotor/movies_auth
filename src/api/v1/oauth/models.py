from flask_restx import Model, fields

oauth_url = Model(
    'OAuthUrl',
    {
        'url': fields.String(required=True)
    }
)
