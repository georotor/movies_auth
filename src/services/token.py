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
    def create(user_id: UUID, user_agent: str, fresh: bool = True):
        """Создаем новую пару access и refresh токенов. Записываем refresh
        токен в redis. Ключом выступает строка из user_agent и jti (unique
        identifier of an encoded JWT).

        Токены нужны для автоматического подтверждения аутентификации, без
        повторного запроса учетных данных. Для доступа к особо чувствительным
        данным у владельцев "не свежих" токенов можно повторно запросить ввод
        пароля. За "свежесть" токена (fresh) отвечает одноименный параметр.

        Args:
          user_id: id пользователя из БД;
          user_agent: id клиентского приложения для формирования ключа в Redis;
          fresh: "свежесть" токена.

        """
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(identity=user_id)

        key = ':'.join((user_agent, get_jti(refresh_token)))
        rd.set(key, str(user_id), ex=config.JWT_REFRESH_TOKEN_EXPIRES)

        return access_token, refresh_token

    @staticmethod
    def delete(user_agent: str) -> str:
        """Отзываем токен. Вносим его в черный список, время жизни записи равно
        времени жизни самого токена.

        Args:
          user_agent: id клиентского приложения для формирования ключа в Redis.
        Returns:
            Тип удаленного токена.

        """
        token = get_jwt()
        key = ':'.join((token["jti"], user_agent))
        rd.set(key, "", ex=config.JWT_ACCESS_TOKEN_EXPIRES)
        return token["type"]

    @staticmethod
    def check_owner(user_agent):
        """Проверяем владельца токена. При выдаче refresh токена создается
        запись в БД. Ключом выступает связка user_agent + jti, значением -
        identity (равное у нас user_id). Проверяем, не изменились ли эти данные
        на текущий момент.

        Args:
          user_agent: id клиентского приложения для формирования ключа в Redis.

        """
        token = get_jwt()
        jti = token["jti"]
        identity = get_jwt_identity()
        key = ':'.join((user_agent, jti))
        return identity == rd.get(key, None)

    @staticmethod
    def refresh(user_agent):
        """Перевыпускаем пару access и refresh токенов. Значение fresh ставим в
        False (токен был сгенерирован автоматически, без повторного ввода
        пользователем учетных данных).

        Args:
          user_agent: id клиентского приложения для формирования ключа в Redis.

        """
        identity = get_jwt_identity()
        return TokenService.create(identity, user_agent, fresh=False)
