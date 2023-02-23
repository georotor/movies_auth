import pytest
from http import HTTPStatus
from faker import Faker

fake: Faker = Faker()
pytestmark = pytest.mark.asyncio


@pytest.fixture(scope='session')
async def user_tokens(make_json_request):
    res = []

    for _ in range(2):
        email = fake.ascii_free_email()
        response = await make_json_request(
            url=f'/api/v1/user/signup',
            json={"email": email, "password": "123password"}
        )
        res.append({
            'email': email,
            **response.body
        })

    yield res


async def test_user_signup(make_json_request):
    response = await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": fake.ascii_free_email(), "password": "123password"}
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
    email = fake.ascii_free_email()
    await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": email, "password": "123password"}
    )

    response = await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": email, "password": "123password"}
    )

    assert response.status == HTTPStatus.CONFLICT


async def test_user_login(make_json_request):
    email = fake.ascii_free_email()
    await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": email, "password": "123password"}
    )

    response = await make_json_request(
        url=f'/api/v1/user/login',
        json={"email": email, "password": "123password"}
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
    email = fake.ascii_free_email()
    await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": email, "password": "123password"}
    )

    response = await make_json_request(
        url=f'/api/v1/user/login',
        json={"email": email, "password": "123"}
    )

    assert response.status == HTTPStatus.BAD_REQUEST


async def test_user_login_invalid_email(make_json_request):
    email = fake.ascii_free_email()
    await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": email, "password": "123password"}
    )

    response = await make_json_request(
        url=f'/api/v1/user/login',
        json={"email": 's'+email, "password": "123password"}
    )

    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_user_login_bad_invalid_password(make_json_request):
    email = fake.ascii_free_email()
    await make_json_request(
        url=f'/api/v1/user/signup',
        json={"email": email, "password": "123password"}
    )

    response = await make_json_request(
        url=f'/api/v1/user/login',
        json={"email": email, "password": "123password123"}
    )

    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_user_update_password(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/update',
        json={"password": "123password123"},
        auth_token=user_tokens[0]['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.OK


async def test_user_update_short_password(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/update',
        json={"password": "ss"},
        auth_token=user_tokens[0]['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.BAD_REQUEST


async def test_user_update_email(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/update',
        json={"email": 's'+user_tokens[0]['email']},
        auth_token=user_tokens[0]['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.OK


async def test_user_update_bad_email(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/update',
        json={"email": "authtest.com"},
        auth_token=user_tokens[0]['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.BAD_REQUEST


async def test_user_update_exist_email(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/update',
        json={"email": user_tokens[1]['email']},
        auth_token=user_tokens[0]['access']['token'],
        method='PATCH'
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_user_history(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/history',
        json={"page_number": 1, "page_size": 10},
        auth_token=user_tokens[0]['access']['token'],
        method='GET'
    )

    assert len(response.body) > 0
    assert response.status == HTTPStatus.OK


async def test_user_history_not_auth(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/history',
        json={'page_number': 1},
        method='GET'
    )

    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_user_refresh_with_access(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/refresh',
        auth_token=user_tokens[0]['access']['token'],
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_user_refresh_with_not_valid(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/refresh',
        auth_token=user_tokens[0]['refresh']['token']+'s',
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_user_refresh(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/refresh',
        auth_token=user_tokens[0]['refresh']['token'],
    )

    assert 'access' in response.body
    assert 'refresh' in response.body
    assert response.status == HTTPStatus.CREATED


async def test_user_logout_not_valid(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/logout',
        auth_token=user_tokens[0]['refresh']['token'],
        method='DELETE'
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_user_logout(make_json_request, user_tokens):
    response = await make_json_request(
        url=f'/api/v1/user/logout',
        auth_token=user_tokens[0]['access']['token'],
        method='DELETE'
    )

    assert response.status == HTTPStatus.OK

    response = await make_json_request(
        url=f'/api/v1/user/history',
        auth_token=user_tokens[0]['access']['token'],
        json={'page_number':1},
        method='GET'
    )

    assert response.status == HTTPStatus.UNAUTHORIZED

    response = await make_json_request(
        url=f'/api/v1/user/refresh',
        auth_token=user_tokens[0]['refresh']['token'],
    )

    assert response.status == HTTPStatus.UNAUTHORIZED
