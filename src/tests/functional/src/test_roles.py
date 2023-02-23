import pytest
from http import HTTPStatus
from faker import Faker

fake: Faker = Faker()
pytestmark = pytest.mark.asyncio


async def test_create_role(make_json_request, user_tokens):
    name = fake.job()
    description = fake.text()

    response = await make_json_request(
        url='/api/v1/roles',
        json={"name": name, "description": description},
        auth_token=user_tokens['admin']['access']['token']
    )

    assert response.status == HTTPStatus.CREATED
    assert response.body['name'] == name
    assert response.body['description'] == description


async def test_create_role_not_admin(make_json_request, user_tokens):
    name = fake.job()
    description = fake.text()

    response = await make_json_request(
        url='/api/v1/roles',
        json={"name": name, "description": description},
        auth_token=user_tokens['user']['access']['token']
    )

    assert response.status == HTTPStatus.FORBIDDEN


async def test_create_duplicate_role(make_json_request, user_tokens):
    name = fake.job()
    description = fake.text()

    await make_json_request(
        url='/api/v1/roles',
        json={"name": name, "description": description},
        auth_token=user_tokens['admin']['access']['token']
    )
    response = await make_json_request(
        url='/api/v1/roles',
        json={"name": name, "description": description},
        auth_token=user_tokens['admin']['access']['token']
    )

    assert response.status == HTTPStatus.CONFLICT


async def test_get_roles(make_json_request, user_tokens):
    response = await make_json_request(
        url='/api/v1/roles',
        auth_token=user_tokens['admin']['access']['token'],
        method='GET'
    )

    assert len(response.body) > 0
    assert response.status == HTTPStatus.OK


async def test_get_roles_not_admin(make_json_request, user_tokens):
    response = await make_json_request(
        url='/api/v1/roles',
        auth_token=user_tokens['user']['access']['token'],
        method='GET'
    )

    assert response.status == HTTPStatus.FORBIDDEN


async def test_update_role(make_json_request, user_tokens):
    name = fake.job()
    description = fake.text()
    token = user_tokens['admin']['access']['token']
    response = await make_json_request(
        url='/api/v1/roles',
        json={'name': name, 'description': description},
        auth_token=token
    )
    role_id = response.body['id']

    response = await make_json_request(
        url=f'/api/v1/roles/{role_id}',
        json={'name': f'updated {name}'},
        auth_token=token,
        method='PATCH'
    )

    assert response.status == HTTPStatus.OK

    response = await make_json_request(
        url=f'/api/v1/roles/{role_id}',
        json={'description': f'updated {description}'},
        auth_token=token,
        method='PATCH'
    )

    assert response.status == HTTPStatus.OK

    response = await make_json_request(
        url='/api/v1/roles',
        auth_token=token,
        method='GET'
    )
    role = next(item for item in response.body if item['id'] == role_id)

    assert role['name'] == f'updated {name}'
    assert role['description'] == f'updated {description}'


async def test_update_role_on_exists(make_json_request, user_tokens):
    name = fake.job()
    token = user_tokens['admin']['access']['token']
    await make_json_request(
        url='/api/v1/roles',
        json={'name': name},
        auth_token=token
    )
    response = await make_json_request(
        url='/api/v1/roles',
        json={'name': f'Two {name}'},
        auth_token=token
    )
    role_id = response.body['id']

    response = await make_json_request(
        url=f'/api/v1/roles/{role_id}',
        json={'name': name},
        auth_token=token,
        method='PATCH'
    )

    assert response.status == HTTPStatus.CONFLICT


async def test_update_role_not_admin(make_json_request, user_tokens):
    role_id = fake.uuid4()

    response = await make_json_request(
        url=f'/api/v1/roles/{role_id}',
        json={'name': 'name'},
        auth_token=user_tokens['user']['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.FORBIDDEN


async def test_delete_role(make_json_request, user_tokens):
    response = await make_json_request(
        url='/api/v1/roles',
        json={"name": "Test delete role"},
        auth_token=user_tokens['admin']['access']['token']
    )
    role_id = response.body["id"]

    response = await make_json_request(
        url=f'/api/v1/roles/{role_id}',
        auth_token=user_tokens['admin']['access']['token'],
        method='DELETE'
    )

    assert response.status == HTTPStatus.OK

    response = await make_json_request(
        url=f'/api/v1/roles/{role_id}',
        json={"name": "Test delete role"},
        auth_token=user_tokens['admin']['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.NOT_FOUND


async def test_delete_unknown_role(make_json_request, user_tokens):
    role_id = fake.uuid4()

    response = await make_json_request(
        url=f'/api/v1/roles/{role_id}',
        auth_token=user_tokens['admin']['access']['token'],
        method='DELETE'
    )

    assert response.status == HTTPStatus.NOT_FOUND


async def test_delete_not_admin(make_json_request, user_tokens):
    role_id = fake.uuid4()

    response = await make_json_request(
        url=f'/api/v1/roles/{role_id}',
        auth_token=user_tokens['user']['access']['token'],
        method='DELETE'
    )

    assert response.status == HTTPStatus.FORBIDDEN
