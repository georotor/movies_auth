import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import db
from utils import utc


users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.UUID, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.UUID, db.ForeignKey('roles.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column('password', db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False, default=utc())
    modified = db.Column(db.DateTime, nullable=False, default=utc(), onupdate=utc())

    history = relationship('UserHistory')
    roles = db.relationship('Role', secondary=users_roles, lazy='subquery',
        backref=db.backref('users', lazy=True))

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).one_or_none()

    def __repr__(self):
        return f'<User {self.email}>'


class UserHistory(db.Model):
    __tablename__ = 'user_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    user_agent = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=utc())


class SocialAccount(db.Model):
    __tablename__ = 'social_account'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User, backref=db.backref('social_accounts', lazy=True))

    social_id = db.Column(db.String(255), nullable=False)
    social_name = db.Column(db.String(50), nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'),)

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'
