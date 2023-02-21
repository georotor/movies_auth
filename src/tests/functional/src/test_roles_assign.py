import pytest
import json
from http.server import HTTPStatus
import requests
from faker import Faker

fake: Faker = Faker()
roles_url = f'http://localhost:5000/api/v1/roles'
assign_url = f'http://localhost:5000/api/v1/roles/assign'
user_url = f'http://localhost:5000/api/v1/user'

# @pytest.fixture(scope='session')
# def create_roles():
#     for _ in range(10):
#         name = fake.job()
#         description = fake.text()

#         response = requests.post(url=roles_url, json={"name": name, "description": description})

#     response = requests.get(url=roles_url)
#     yield response.json()

    # response = requests.get(url=roles_url)
    # for role in response.json():
    #     role_id = role.get('id')
    #     response = requests.delete(url=f"{roles_url}/{role_id}")
    #     response.status_code == HTTPStatus.OK



# @pytest.fixture(scope='session')
# def test_create_users():
#     for _ in range(10):
#         email = fake.email()
#         password = fake.password()

#         response = requests.post(f'{user_url}/signup', json={"email": email, "password": password})


@pytest.fixture(scope='session')
def get_admin_tokens():
    email = "admin@admin.com"
    password = "admin123"

    response = requests.post(f'{user_url}/login', json={"email": email, "password": password})

    yield response.json()

@pytest.fixture(scope='session')
def get_user_tokens():
    email = "user@user.com"
    password = "user1234"

    response = requests.post(f'{user_url}/login', json={"email": email, "password": password})

    yield response.json()

def test_assign_role_without_auth_header():
    role_id = "4cd6adcd-abf9-44e6-90a9-65f32782d25d"
    user_id = "1a99b6f3-65d8-454c-86f8-05455fb7d000"

    response = requests.post(assign_url, json={'user_id': user_id, 'role_id': role_id})

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.parametrize(
    'user_id, role_id', [
        (
            "1a99b6f3-65d8-454c-86f8-05455fb7d000",
            "4cd6adcd-abf9-44e6-90a9-65f32782d25d"
        ),
        (
            "7d81309f-2345-40e9-8c71-ece70cd0e830",
            "58eeb22b-282a-460b-914b-b37550fb61df"
        ),
        (
            "c2d7d0c2-fe2b-4720-8fb8-1fd057a832ca",
            "317dc742-7656-48e8-ace5-c3eb0da2cffb"
        )
    ]
)
def test_assign_role_with_admin_token(get_admin_tokens, user_id, role_id):
    access_token = get_admin_tokens['access']['token']

    response = requests.post(assign_url, json={'user_id': user_id, 'role_id': role_id}, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == HTTPStatus.OK

#@pytest.mark.xfail()
def test_assign_role_without_admin_token(get_user_tokens):
    user_id = "1a99b6f3-65d8-454c-86f8-05455fb7d000"
    role_id = "4cd6adcd-abf9-44e6-90a9-65f32782d25d"
    access_token = get_user_tokens['access']['token']

    response = requests.post(assign_url, json={'user_id': user_id, 'role_id': role_id}, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == HTTPStatus.FORBIDDEN

def test_assign_role_that_doesnt_exist(get_admin_tokens):
    user_id = "c2d7d0c2-fe2b-4720-8fb8-1fd057a832ca"
    role_id = "00000000-0000-0000-0000-000000000000"
    access_token = get_admin_tokens['access']['token']

    response = requests.post(assign_url, json={'user_id': user_id, 'role_id': role_id}, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == HTTPStatus.NOT_FOUND

def test_assign_role_to_user_that_doesnt_exist(get_admin_tokens):
    user_id = "00000000-0000-0000-0000-000000000000"
    role_id = "317dc742-7656-48e8-ace5-c3eb0da2cffb"
    access_token = get_admin_tokens['access']['token']

    response = requests.post(assign_url, json={'user_id': user_id, 'role_id': role_id}, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == HTTPStatus.NOT_FOUND


# def test_create_roles():
#     for _ in range(3):
#         name = fake.job()
#         description = fake.text()

#         response = requests.post(url=roles_url, json={"name": name, "description": description})

#         assert response.status_code == HTTPStatus.CREATED
#         assert response.json()['name'] == name
#         assert response.json()['description'] == description

# def test_create_duplicate_role():
#     name = fake.job()
#     description = fake.text()

#     requests.post(url=roles_url, json={"name": name, "description": description})
#     response = requests.post(url=roles_url, json={"name": name, "description": description})

#     assert response.status_code == HTTPStatus.CONFLICT


# def test_get_roles():
#     response = requests.get(url=roles_url)

#     assert 'name' in response.json()[0]
#     assert 'description' in response.json()[0]
#     assert response.status_code == HTTPStatus.OK

# def test_delete_role():
#     response = requests.get(url=roles_url)
#     role_id = response.json()[0]['id']

#     response = requests.delete(url=f"{roles_url}/{role_id}")

#     assert response.status_code == HTTPStatus.OK

# def test_delete_unknown_role():
#     role_id = fake.uuid4()

#     response = requests.delete(url=f"{roles_url}/{role_id}")

#     assert response.status_code == HTTPStatus.NOT_FOUND


# def test_delete_roles():
#     response = requests.get(url=roles_url)
#     for role in response.json():
#         role_id = role.get('id')
#         response = requests.delete(url=f"{roles_url}/{role_id}")
#         response.status_code == HTTPStatus.OK