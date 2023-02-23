from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_redis import Redis


db = SQLAlchemy()
ma = Marshmallow()
rd = Redis()
