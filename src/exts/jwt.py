import logging

from flask_jwt_extended import JWTManager

from db import rd
from models.user import User

logger = logging.getLogger(__name__)
jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """Callback, используется flask-jwt-extended для проверки статуса токена.
    https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking/#redis

    """
    key = jwt_payload["jti"]
    token_in_redis = rd.get(key)
    if token_in_redis:
        logger.info('Токен (type:{}) пользователя <{}> в стоп листе'.format(jwt_payload['type'], jwt_payload['sub']))
    return token_in_redis is not None


@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    """Callback, используется при создании токена с дополнительными данными.
    https://flask-jwt-extended.readthedocs.io/en/latest/add_custom_data_claims/

    В данном случае используем его для хранения флага is_admin, теоретически
    сюда можно положить список всех ролей пользователя.

    """
    user = User.query.filter_by(id=identity).one_or_none()
    return {'is_admin': user.is_admin}