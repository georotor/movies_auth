import pytest
import json
from http.server import HTTPStatus
import requests

@pytest.mark.asyncio
async def test_first_signup(make_post_request):
    data = json.dumps({"email": "email@test.ru", "password": "password"}).encode()
    response = await make_post_request(url=f'/api/v1/user/signup', data=data)
    assert response.status == HTTPStatus.OK

@pytest.mark.asyncio
async def test_signup_again(make_post_request):
    data = json.dumps({"email": "email", "password": "password"}).encode()
    response = await make_post_request(url=f'/api/v1/user/signup', data=data)
    assert response.status == HTTPStatus.BAD_REQUEST
