from datetime import datetime, timezone


def utc():
    return datetime.now(timezone.utc)
