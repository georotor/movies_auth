from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import redis
from config import Config

db = SQLAlchemy()
ma = Marshmallow()
config = Config()

rd = redis.Redis.from_url(
    "{}:{}".format(config.REDIS_HOST, config.REDIS_PORT),
    decode_responses=True,
)
