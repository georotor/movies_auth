from functools import lru_cache, wraps
from http import HTTPStatus
import logging
from typing import Optional
from uuid import UUID

from flask import abort
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from sqlalchemy import insert, select
from sqlalchemy.exc import NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from models.user import User, UserHistory, db
from schemas.user import (LoginSchema, RegistrationSchema, UpdateUserSchema,
                          UserHistorySchema)


logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Исключение для ошибок при аутентификации пользователя."""


class UserService:
    """Сервис аутентификации. Несколько статических методов, которые объеденины
    в один класс просто для удобства.

    """

    @staticmethod
    def find_user(email: str) -> Optional[User]:
        """Проверяем наличие пользователя с указанным email."""
        try:
            return db.session.scalars(
                select(User).where(User.email == email)
            ).one()
        except NoResultFound:
            logger.debug('Не найден пользователь {}'.format(email))
            return

    @staticmethod
    def login(data: dict):
        """Аутентификация пользователя. Валидация данных перенесена в restx и
        убрана из схемы.

        """
        auth_data = LoginSchema().load(data)
        user = UserService.find_user(auth_data.email)
        if user is None:
            raise AuthError("No such user")

        if not check_password_hash(user.password, auth_data.password):
            logger.debug('Неверный пароль для {}'.format(auth_data.email))
            raise AuthError("Invalid username or password")

        logger.info('Успешная аутентификация {}'.format(auth_data.email))
        return user.id

    @staticmethod
    def registration(data: dict):
        """Регистрация пользователя. Валидация данных (включая требования к
        сложности пароля) перенесена в restx и убрана из схемы.

        Если пользователь с таким email уже существует - поднимаем исключение
        AuthError.

        """
        new_user = RegistrationSchema().load(data)

        if UserService.find_user(new_user.email) is not None:
            logger.debug('Попытка регистрации с занятым email {}'.format(
                new_user.email
            ))
            raise AuthError("Email already in use")

        db.session.execute(
            insert(User).values(
                email=new_user.email,
                password=generate_password_hash(new_user.password),
            )
        )
        db.session.commit()
        logger.debug('Регистрация нового пользователя {}'.format(
            new_user.email
        ))
        user = UserService.find_user(new_user.email)
        return user.id

    @staticmethod
    def update_user(data):
        new_user = UpdateUserSchema().load(data)
        user = User.query.filter_by(id=new_user.id).one_or_none()
        if user is None:
            raise AuthError("No such user")

        if new_user.email != user.email:
            if UserService.find_user(new_user.email) is not None:
                logger.debug('Обновление данных {}: email {} занят'.format(
                    new_user.id, new_user.email
                ))
                raise ValueError("Email already in use")

        if new_user.password:
            user.password = generate_password_hash(new_user.password)
            logger.info('Пользователь {} изменил пароль'.format(
                new_user.id
            ))

        if new_user.email:
            user.email = new_user.email
            logger.info('Пользователь {} изменил email на {}'.format(
                new_user.id, new_user.email
            ))

        if db.session.is_modified(user):
            db.session.commit()

    @staticmethod
    def remember_login(user_id: UUID, user_agent: str, action: str = 'login'):
        """Запись о логине пользователя. Валидация данных перенесена в restx и
        убрана из схемы.

        Args:
          user_id: id пользователя из БД;
          user_agent: id клиентского приложения для формирования ключа в Redis;
          action: тип события.

        """
        history_data = {
            'user_id': user_id,
            'user_agent': user_agent,
            'action': action,
        }
        new_log = UserHistorySchema().load(history_data)
        db.session.execute(
            insert(UserHistory).values(
                user_id=new_log.user_id,
                user_agent=new_log.user_agent,
                action=new_log.action,
            )
        )
        logger.debug('Запись данных о входе: {}'.format(history_data))
        db.session.commit()
    @staticmethod
    def login_history(user_id, page_number=1, page_size=10):
        """Список 10 последних записей входа. """
        offset = page_number - 1
        raw_data = db.session.scalars(
            select(UserHistory).where(UserHistory.user_id == user_id).order_by(
                UserHistory.created.desc()
            ).limit(page_size).offset(offset * page_size)
        ).all()
        history = UserHistorySchema().dump(raw_data, many=True)
        logger.debug('Запрос истории для {}'.format(user_id))
        return history


def admin_required():
    """Декоратор, проверяющий наличие записи о правах администратора в claims.

    https://flask-jwt-extended.readthedocs.io/en/stable/custom_decorators/

    """
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_id = get_jwt_identity()
            if not claims["is_admin"]:
                logger.debug(
                    'Пользователь {}: попытка неправомерного доступа'.format(
                        user_id
                    ))
                abort(HTTPStatus.FORBIDDEN, 'Access denied')
            return func(*args, **kwargs)
        return decorator
    return wrapper


@lru_cache()
def get_user_service() -> UserService:
    return UserService()


