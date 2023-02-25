from functools import lru_cache
from config import Config

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://{}:{}".format(Config.REDIS_HOST, Config.REDIS_PORT),
)


@lru_cache()
def get_limiter() -> Limiter:
    return limiter
