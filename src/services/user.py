from functools import lru_cache, wraps
from http import HTTPStatus
import logging
import secrets
from typing import Optional
from uuid import UUID

from flask import abort
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from sqlalchemy import insert, select
from sqlalchemy.exc import NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from models.user import User, UserHistory, SocialAccount, db
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
    def find_user_by_social(social_id: str, social_name: str) -> Optional[SocialAccount]:
        """Проверяем наличие пользователя."""
        try:
            return db.session.scalars(
                select(User)
                .join(SocialAccount.user)
                .where(
                    SocialAccount.social_id == social_id,
                    SocialAccount.social_name == social_name
                )
            ).one()
        except NoResultFound:
            logger.debug('Не найден пользователь social_id: {}, social_name: {}'.format(
                social_id, social_name
            ))
            return None

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
            logger.debug('Неверный пароль для пользователя <{}>'.format(user.id))
            raise AuthError("Invalid username or password")

        logger.info('Успешная аутентификация <{}>'.format(user.id))
        return user.id

    def registration_social(self, email: str, social_id: str, social_name: str):
        """
        Регистрация пользователя с привязкой к внешним сервисам авторизации.
        :param email: Email нового пользователя
        :param social_id: Индификатор во внешнем сервисе авторизации
        :param social_name: Название внешнего сервиса авторизации
        :return: Объект пользователя
        """
        user = self.find_user(email)
        if not user:
            user = self.registration({
                'email': email,
                'password': secrets.token_urlsafe(13)
            })

        db.session.execute(
            insert(SocialAccount).values(
                user_id=user.id,
                social_id=social_id,
                social_name=social_name
            )
        )
        db.session.commit()

        logger.debug('Зарегистрирован пользователь <{}> из сети <{}>'.format(
            social_id, social_name
        ))

        return user

    @staticmethod
    def registration(data: dict):
        """Регистрация пользователя. Валидация данных (включая требования к
        сложности пароля) перенесена в restx и убрана из схемы.

        Если пользователь с таким email уже существует - поднимаем исключение
        AuthError.

        """
        new_user = RegistrationSchema().load(data)

        exist_user = UserService.find_user(new_user.email)
        if exist_user is not None:
            logger.debug('Попытка регистрации с занятым email <{}>'.format(
                exist_user.id
            ))
            raise AuthError("Email already in use")

        db.session.execute(
            insert(User).values(
                email=new_user.email,
                password=generate_password_hash(new_user.password),
            )
        )
        db.session.commit()
        user = UserService.find_user(new_user.email)
        logger.debug('Регистрация нового пользователя <{}>'.format(
            user.id
        ))
        return user

    @staticmethod
    def update_user(data):
        new_user = UpdateUserSchema().load(data)
        user = User.query.filter_by(id=new_user.id).one_or_none()
        if user is None:
            raise AuthError("No such user")

        if new_user.email != user.email:
            exist_user = UserService.find_user(new_user.email)
            if exist_user is not None:
                logger.debug('Обновление данных <{}>: email занят <{}>'.format(
                    new_user.id, exist_user.id
                ))
                raise ValueError("Email already in use")

        if new_user.password:
            user.password = generate_password_hash(new_user.password)
            logger.info('Пользователь <{}> изменил пароль'.format(
                new_user.id
            ))

        if new_user.email:
            user.email = new_user.email
            logger.info('Пользователь <{}> изменил email'.format(
                new_user.id
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
        logger.debug('Запись данных о входе <{}>'.format(user_id))
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


