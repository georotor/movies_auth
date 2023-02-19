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
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(identity=user_id)

        key = get_jti(refresh_token)
        rd.set(key, str(user_id), ex=config.JWT_REFRESH_TOKEN_EXPIRES)

        return access_token, refresh_token

    @staticmethod
    def delete() -> str:
        """Отзываем токен. Вносим его в черный список, время жизни записи равно
        времени жизни самого токена.

        Returns:
            Тип удаленного токена.

        """
        token = get_jwt()
        rd.set(token["jti"], "", ex=config.JWT_ACCESS_TOKEN_EXPIRES)
        return token["type"]

    @staticmethod
    def refresh():
        """Перевыпускаем пару access и refresh токенов. Значение fresh ставим в
        False (токен был сгенерирован автоматически, без повторного ввода
        пользователем учетных данных).

        """
        identity = get_jwt_identity()
        return TokenService.create(identity, fresh=False)
