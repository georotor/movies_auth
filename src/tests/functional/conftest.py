import asyncio
import base64
import json
import pytest
from faker import Faker

fake: Faker = Faker()

pytest_plugins = ("tests.functional.utils.fixtures.http",)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def user_tokens(make_json_request):
    url = '/api/v1/user/login'
    users = {
        'user': (await make_json_request(url=url, json={"email": "user@roles.test", "password": "123qweasd"})).body,
        'admin': (await make_json_request(url=url, json={"email": "admin@roles.test", "password": "123qweasd"})).body
    }

    for user in users:
        s = users[user]['access']['token'].split('.')[1]
        payload = base64.b64decode(s + '=' * (-len(s) % 4))
        users[user]['id'] = json.loads(payload)['sub']

    yield users


@pytest.fixture(scope='session')
async def roles(make_json_request, user_tokens):
    roles_list = []
    for _ in range(2):
        response = await make_json_request(
            url=f'/api/v1/roles',
            json={"name": fake.job(), "description": fake.text()},
            auth_token=user_tokens['admin']['access']['token']
        )
        roles_list.append(response.body)

    yield roles_list

    for role in roles_list:
        await make_json_request(
            url=f'/api/v1/roles/{role["id"]}',
            auth_token=user_tokens['admin']['access']['token'],
            method='DELETE'
        )
