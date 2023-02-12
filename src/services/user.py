from functools import lru_cache

from models.user import User, db
from services.token import TokenService


class UserService:
    def __init__(self):
        self.id = None

    def create(self, email: str, password: str):
        """
        Создаем нового пользователя.

        :param email: Используется как логин.
        :param password: Пароль нового пользователя.
        :return: Access и refresh токены или None, если такой пользователь уже есть
        """
        if User.find_by_email(email):
            return None

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        self.id = new_user.id

        return TokenService.create(user=new_user)


@lru_cache()
def get_user_service() -> UserService:
    return UserService()
