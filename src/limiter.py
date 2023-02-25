from ipaddress import IPv4Address
from functools import lru_cache
from config import Config

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def except_localhost():
    """Исключаем limit rate для подключений с localhost. Может быть нужно для
    работы тестов.

    """
    remote_address = get_remote_address()
    if IPv4Address(remote_address).is_loopback:
        return True
    return False


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10000 per day", "1000 per hour"],
    storage_uri="redis://{}:{}".format(Config.REDIS_HOST, Config.REDIS_PORT),
    default_limits_exempt_when=except_localhost,
)


@lru_cache()
def get_limiter() -> Limiter:
    return limiter
