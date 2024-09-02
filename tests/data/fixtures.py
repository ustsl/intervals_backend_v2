import pytest

from tests.conftest import client
from tests.user.fixtures import login_user


@pytest.fixture(scope="session")
def create_data_fixture():
    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}

    response = client.post(
        "/data",
        json={"title": "data fixtures", "container": {"data": "data"}},
        headers=headers,
    )

    data = response.json()
    assert response.status_code == 201
    assert data.get("title") == "data fixtures"
    return data
