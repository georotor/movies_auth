import pytest
from http import HTTPStatus
from faker import Faker

fake: Faker = Faker()
pytestmark = pytest.mark.asyncio


async def test_roles_assign_add_role(make_json_request, user_tokens, roles):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": user_tokens['admin']['id'], "role_id": roles[0]['id']},
        auth_token=user_tokens['admin']['access']['token']
    )

    assert response.status == HTTPStatus.OK


async def test_roles_assign_check_role(make_json_request, user_tokens, roles):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": user_tokens['admin']['id'], "role_id": roles[0]['id']},
        auth_token=user_tokens['admin']['access']['token'],
        method='GET'
    )

    assert response.status == HTTPStatus.OK


async def test_roles_assign_check_not_role(make_json_request, user_tokens, roles):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": user_tokens['admin']['id'], "role_id": roles[1]['id']},
        auth_token=user_tokens['admin']['access']['token'],
        method='GET'
    )

    assert response.status == HTTPStatus.NOT_FOUND


async def test_roles_assign_delete_role(make_json_request, user_tokens, roles):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": user_tokens['admin']['id'], "role_id": roles[0]['id']},
        auth_token=user_tokens['admin']['access']['token'],
        method='GET'
    )

    assert response.status == HTTPStatus.OK


@pytest.mark.parametrize('method', ['POST', 'GET', 'DELETE'])
async def test_roles_assign_add_user_not_found(make_json_request, user_tokens, roles, method):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": fake.uuid4(), "role_id": roles[0]['id']},
        auth_token=user_tokens['admin']['access']['token'],
        method=method
    )

    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize('method', ['POST', 'GET', 'DELETE'])
async def test_roles_assign_role_not_found(make_json_request, user_tokens, roles, method):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": user_tokens['admin']['id'], "role_id": fake.uuid4()},
        auth_token=user_tokens['admin']['access']['token'],
        method=method
    )

    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize('method', ['POST', 'GET', 'DELETE'])
async def test_roles_assign_user_not_valid(make_json_request, user_tokens, roles, method):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": 11, "role_id": fake.uuid4()},
        auth_token=user_tokens['admin']['access']['token'],
        method=method
    )

    assert response.status == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize('method', ['POST', 'GET', 'DELETE'])
async def test_roles_assign_role_not_valid(make_json_request, user_tokens, roles, method):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": fake.uuid4(), "role_id": 11},
        auth_token=user_tokens['admin']['access']['token'],
        method=method
    )

    assert response.status == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize('method', ['POST', 'GET', 'DELETE'])
async def test_roles_assign_forbidden(make_json_request, user_tokens, roles, method):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": user_tokens['admin']['id'], "role_id": roles[0]['id']},
        auth_token=user_tokens['user']['access']['token'],
        method=method
    )

    assert response.status == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize('method', ['POST', 'GET', 'DELETE'])
async def test_roles_assign_token_not_valid(make_json_request, user_tokens, roles, method):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": user_tokens['admin']['id'], "role_id": roles[0]['id']},
        auth_token='qwe',
        method=method
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize('method', ['POST', 'GET', 'DELETE'])
async def test_roles_assign_not_token(make_json_request, user_tokens, roles, method):
    response = await make_json_request(
        url='/api/v1/roles/assign',
        json={"user_id": user_tokens['admin']['id'], "role_id": roles[0]['id']},
        method=method
    )

    assert response.status == HTTPStatus.UNAUTHORIZED
