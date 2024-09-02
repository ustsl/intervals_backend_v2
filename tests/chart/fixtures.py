import pytest

from tests.conftest import client
from tests.user.fixtures import login_user


@pytest.fixture(scope="session")
def create_chart_fixture():
    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}

    response = client.post(
        "/data",
        json={"title": "data fixtures", "container": {"data": "data"}},
        headers=headers,
    )

    data = response.json()
    data_id = data.get("id")

    response = client.post(
        "/chart",
        json={
            "title": "chart fixture 1",
            "data": data_id,
            "settings": {"axisX": "213", "axisY": [{"field": "ss", "type": "dsf"}]},
        },
        headers=headers,
    )

    data = response.json()
    assert response.status_code == 201
    assert data.get("title") == "chart fixture 1"
    return data
