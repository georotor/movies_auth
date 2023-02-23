from dataclasses import dataclass

import aiohttp
import pytest
from multidict import CIMultiDictProxy

from tests.functional.settings import test_settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def session():
    """ Единая сессия для всех тестов. """
    client_session = aiohttp.ClientSession()
    yield client_session
    await client_session.close()


@pytest.fixture(scope='session')
def make_json_request(session):
    """
    Фикстура для выполнения запросов.

    :param session: Клиент aiohttp.
    :return: Функция выполнения POST запросов.
    """
    async def inner(
            url: str,
            json: dict | None = None,
            headers: dict | None = None,
            auth_token: str | None = None,
            method: str = 'POST'
    ):
        json = json or {}
        headers = headers or {'Content-Type': 'application/json'}
        if auth_token:
            headers['Authorization'] = f'Bearer {auth_token}'
        url = test_settings.service_url + url
        async with session.request(method, url, json=json, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner
