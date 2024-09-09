import pytest

from tests.conftest import client

TEST_EMAIL = "test@imvo.site"
TEST_PASSWORD = "CokZorKelime123"


@pytest.fixture(scope="module")
def create_user_fuxture():
    response = client.post(
        "/auth/register",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )
    data = response.json()
    get_account()
    return data


def get_account():
    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}
    response = client.get("/account/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("is_active")


def login_user():
    response = client.post(
        "/auth/jwt/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("access_token")
    return data.get("access_token")
