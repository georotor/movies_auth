import pytest
import json
from http.server import HTTPStatus
import requests
from faker import Faker

fake = Faker()

@pytest.mark.asyncio
async def test_first_signup(make_post_request):
    email = fake.email()
    password = fake.password()

    response = await make_post_request(url=f'/api/v1/user/signup', data=json.dumps({"email": email, "password": password}).encode())

    assert 'access' in response.body
    assert 'refresh' in response.body
    assert response.status == HTTPStatus.CREATED

@pytest.mark.asyncio
async def test_signup_invalid_email(make_post_request):
    data = json.dumps({"email": "email", "password": "password"}).encode()

    response = await make_post_request(url=f'/api/v1/user/signup', data=data)

    assert response.status == HTTPStatus.BAD_REQUEST

@pytest.mark.asyncio
async def test_signup_invalid_password(make_post_request):
    data = json.dumps({"email": "test@test.ru", "password": "123"}).encode()

    response = await make_post_request(url=f'/api/v1/user/signup', data=data)

    assert response.status == HTTPStatus.BAD_REQUEST
