import pytest

from tests.conftest import client

TEST_EMAIL = "test@imvo.site"
TEST_PASSWORD = "CokZorKelime123"


@pytest.fixture(scope="session")
def create_user_fuxture():
    response = client.post(
        "/auth/register",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )
    data = response.json()
    return data


def login_user():
    response = client.post(
        "/auth/jwt/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("access_token")
    return data.get("access_token")
