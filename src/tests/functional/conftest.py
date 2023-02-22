import asyncio
import pytest


pytest_plugins = ("tests.functional.utils.fixtures.http",)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


# @pytest.fixture(scope="module")
# def clean_db():
#     smtp_connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
#     yield smtp_connection  # provide the fixture value
#     print("teardown smtp")
#     smtp_connection.close()
