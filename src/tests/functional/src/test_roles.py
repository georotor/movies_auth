import pytest
import json
from http.server import HTTPStatus
import requests
from faker import Faker

fake: Faker = Faker()
roles_url = f'http://localhost:5000/api/v1/roles'

def test_create_role():
    name = fake.job()
    description = fake.text()

    response = requests.post(url=roles_url, json={"name": name, "description": description})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == name
    assert response.json()['description'] == description

def test_create_duplicate_role():
    name = fake.job()
    description = fake.text()

    requests.post(url=roles_url, json={"name": name, "description": description})
    response = requests.post(url=roles_url, json={"name": name, "description": description})

    assert response.status_code == HTTPStatus.CONFLICT


def test_get_roles():
    response = requests.get(url=roles_url)

    assert 'name' in response.json()[0]
    assert 'description' in response.json()[0]
    assert response.status_code == HTTPStatus.OK

def test_delete_role():
    response = requests.get(url=roles_url)
    role_id = response.json()[0]['id']

    response = requests.delete(url=f"{roles_url}/{role_id}")

    assert response.status_code == HTTPStatus.OK

def test_delete_unknown_role():
    role_id = fake.uuid4()

    response = requests.delete(url=f"{roles_url}/{role_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND

