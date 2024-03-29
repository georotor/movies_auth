import uuid

from sqlalchemy.dialects.postgresql import UUID

from db import db, ma
from utils import utc


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=utc())
    modified = db.Column(db.DateTime, nullable=False, default=utc(), onupdate=utc())

    def __repr__(self):
        return f'<Roles {self.name}>'


class RoleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')
