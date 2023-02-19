import uuid

from sqlalchemy import ForeignKey, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import db
from utils import utc
from models.role import Role


class User(db.Model):
    """Есть разные способы хэширования паролей. Можно делать это на уровне
    модели БД:

        1) через @property и setter в классе User:

            @property
            def password(self):
                return self._password

            @password.setter
            def password(self, password: str):
                self._password = generate_password_hash(password)

        2) через перехватывание ивента внешней функцией с @event.listens_for

            @event.listens_for(User.password, 'set', retval=True)
            def hash_user_password(target, value, oldvalue, initiator):
                if value != oldvalue:
                    return generate_password_hash(value)
                return value

    Я бы предпочел следовать модели MVC - разделить data plane и control plane.
    В models.py мы описываем таблицы БД, а всю бизнес логику (включая то что и
    каким образом мы шифруем) мы выносим в services. Если в будущем мы решим
    заменить алгоритм шифрования или библиотеку - никаких изменений в
    models.py вносить не придется.

    Аналогично с методом find_by_email - на мой взгляд, ему в ORM не место.
    Нужно выносить в services.

    """
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column('password', db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False, default=utc())
    modified = db.Column(db.DateTime, nullable=False, default=utc(), onupdate=utc())

    history = relationship('UserHistory')
    roles = relationship('UsersRoles')

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).one_or_none()

    def __repr__(self):
        return f'<User {self.email}>'


class UsersRoles(db.Model):
    __tablename__ = 'users_roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    role_id = db.Column(UUID(as_uuid=True), ForeignKey(Role.id))


class UserHistory(db.Model):
    __tablename__ = 'user_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    action = db.Column(db.String, nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=utc())
