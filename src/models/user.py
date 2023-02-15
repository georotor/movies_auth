import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

from db import db
from utils import utc
from models.role import Role


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column('password', db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False, default=utc())
    modified = db.Column(db.DateTime, nullable=False, default=utc(), onupdate=utc())

    history = relationship('UserHistory')
    roles = relationship('UsersRoles')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = generate_password_hash(password)

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
