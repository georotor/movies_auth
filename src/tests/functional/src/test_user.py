import pytest
from http import HTTPStatus

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope='session')
async def user_tokens(make_json_request):
    await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": "authtwo@test.test", "password": "123password"}
    )
    response = await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": "auth@test.test", "password": "123password"}
    )

    yield response.body


async def test_user_signup(make_json_request):
    response = await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": "test@test.test", "password": "123password"}
    )

    assert 'access' in response.body
    assert 'refresh' in response.body
    assert response.status == HTTPStatus.CREATED


async def test_user_signup_bad_email(make_json_request):
    response = await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": "testtest.test", "password": "123password"}
    )

    assert response.status == HTTPStatus.BAD_REQUEST


async def test_user_signup_short_password(make_json_request):
    response = await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": "test@test.test", "password": "123"}
    )

    assert response.status == HTTPStatus.BAD_REQUEST


async def test_user_signup_used_email(make_json_request):
    response = await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": "test@test.test", "password": "123password"}
    )

    assert response.status == HTTPStatus.CONFLICT


async def test_user_login(make_json_request):
    response = await make_json_request(
        url=f'/api/v1/user/login',
        json={"email": "test@test.test", "password": "123password"}
    )

    assert 'access' in response.body
    assert 'refresh' in response.body
    assert response.status == HTTPStatus.OK


async def test_user_login_bad_email(make_json_request):
    response = await make_json_request(
        url=f'/api/v1/user/login',
        json={"email": "testtest.test", "password": "123password"}
    )

    assert response.status == HTTPStatus.BAD_REQUEST


async def test_user_login_bad_short_password(make_json_request):
    response = await make_json_request(
        url=f'/api/v1/user/login',
        json={"email": "test@test.test", "password": "123"}
    )

    assert response.status == HTTPStatus.BAD_REQUEST


async def test_user_login_invalid_email(make_json_request):
    response = await make_json_request(
        url=f'/api/v1/user/login',
        json={"email": "test@tes.test", "password": "123password"}
    )

    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_user_login_bad_invalid_password(make_json_request):
    response = await make_json_request(
        url=f'/api/v1/user/login',
        json={"email": "test@test.test", "password": "123password123"}
    )

    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_user_update_password(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/update',
        json={"password": "123password123"},
        auth_token=user_tokens['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.OK


async def test_user_update_short_password(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/update',
        json={"password": "ss"},
        auth_token=user_tokens['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.BAD_REQUEST


async def test_user_update_email(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/update',
        json={"email": "auth@test.com"},
        auth_token=user_tokens['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.OK


async def test_user_update_bad_email(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/update',
        json={"email": "authtest.com"},
        auth_token=user_tokens['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.BAD_REQUEST


async def test_user_update_exist_email(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/update',
        json={"email": "authtwo@test.test"},
        auth_token=user_tokens['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_user_history(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/history',
        auth_token=user_tokens['access']['token'],
        method='GET'
    )

    assert len(response.body) > 0
    assert response.status == HTTPStatus.OK


async def test_user_history_not_auth(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/history',
        method='GET'
    )

    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_user_refresh_with_access(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/refresh',
        auth_token=user_tokens['access']['token'],
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_user_refresh_with_not_valid(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/refresh',
        auth_token=user_tokens['refresh']['token']+'s',
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_user_refresh(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/refresh',
        auth_token=user_tokens['refresh']['token'],
    )

    assert 'access' in response.body
    assert 'refresh' in response.body
    assert response.status == HTTPStatus.CREATED


async def test_user_logout_not_valid(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/logout',
        auth_token=user_tokens['refresh']['token'],
        method='DELETE'
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_user_logout(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/logout',
        auth_token=user_tokens['access']['token'],
        method='DELETE'
    )

    assert response.status == HTTPStatus.OK

    response = await make_json_request(
        url=f'/api/v1/user/history',
        auth_token=user_tokens['access']['token'],
        method='GET'
    )

    assert response.status == HTTPStatus.UNAUTHORIZED

    response = await make_json_request(
        url=f'/api/v1/user/refresh',
        auth_token=user_tokens['refresh']['token'],
    )

    assert response.status == HTTPStatus.UNAUTHORIZED
