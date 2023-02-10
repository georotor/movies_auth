from datetime import datetime

from flask_jwt_extended import create_refresh_token, create_access_token, decode_token

from models.user import User
from models.token import Token, Tokens


class TokenService:
    @staticmethod
    def create(user: User):
        # TODO: записать в Redis
        refresh_token = create_refresh_token(identity=user.id)
        access_token = create_access_token(identity=user.id)

        return Tokens(
            access=Token(
                token=access_token,
                expired=datetime.utcfromtimestamp(decode_token(access_token)['exp'])
            ),
            refresh=Token(
                token=refresh_token,
                expired=datetime.utcfromtimestamp(decode_token(refresh_token)['exp'])
            ),
        )
