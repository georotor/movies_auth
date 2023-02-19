from datetime import datetime, timezone
from uuid import UUID

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jti, get_jwt, get_jwt_identity)

from config import Config
from db import rd

config = Config()


class TokenError(Exception):
    """Исключение для ошибок при работе с токенами."""


class TokenService:
    @staticmethod
    def create(user_id: UUID, fresh: bool = True):
        """Создаем новую пару access и refresh токенов. Записываем refresh
        токен в redis. Ключом выступает jti (unique identifier of an encoded
        JWT).

        Токены нужны для автоматического подтверждения аутентификации, без
        повторного запроса учетных данных. Для доступа к особо чувствительным
        данным у владельцев "не свежих" токенов можно повторно запросить ввод
        пароля. За "свежесть" токена (fresh) отвечает одноименный параметр.

        Args:
          user_id: id пользователя из БД;
          fresh: "свежесть" токена.

        """
        refresh_token = create_refresh_token(identity=user_id)
        access_token = create_access_token(
            identity=user_id,
            additional_claims={'refresh_jti': get_jti(refresh_token)},
            fresh=fresh,
        )

        key = get_jti(refresh_token)
        rd.set(key, str(user_id), ex=config.JWT_REFRESH_TOKEN_EXPIRES)

        return access_token, refresh_token

    @staticmethod
    def delete():
        """Отзываем access токен и связанный с ним refresh токен. Вносим их в
        черный список, где время жизни записи равно времени жизни токена.

        """
        token = get_jwt()
        rd.set(token["jti"], "", ex=config.JWT_ACCESS_TOKEN_EXPIRES)
        rd.set(token["refresh_jti"], "", ex=config.JWT_REFRESH_TOKEN_EXPIRES)

    @staticmethod
    def refresh():
        """Перевыпускаем пару access и refresh токенов. Значение fresh ставим в
        False (токен был сгенерирован автоматически, без повторного ввода
        пользователем учетных данных).

        """
        identity = get_jwt_identity()
        return TokenService.create(identity, fresh=False)

    @staticmethod
    def expired_at():
        return datetime.now(timezone.utc) + config.JWT_ACCESS_TOKEN_EXPIRES
