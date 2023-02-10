import uuid

from sqlalchemy.dialects.postgresql import UUID

from db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).one_or_none()

    def __repr__(self):
        return f'<User {self.email}>'

