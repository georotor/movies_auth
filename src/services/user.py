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

        return TokenService.create(user_id=new_user.id)

    def login(self, username, password):
        user = User.query.filter_by(email=username).first()
        if not user:
            return
        password_hash = password
        if password_hash != user.password:
            return
        self.id = user.id
        return True

    def log(self, user_host, user_agent):
        """Записываем дату, ip и браузер. """
        pass




@lru_cache()
def get_user_service() -> UserService:
    return UserService()
