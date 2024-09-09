import pytest

from tests.conftest import client
from tests.user.fixtures import login_user


@pytest.fixture(scope="module")
def create_dashboard_fixture():
    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}

    response = client.post(
        "/dashboard",
        json={"title": "test dashboard"},
        headers=headers,
    )

    data = response.json()
    assert response.status_code == 201
    assert data.get("title") == "test dashboard"
    return data


@pytest.fixture(scope="module")
def create_chart_fixture_for_dashboard():
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
            "title": "chart fixture for dashboard",
            "data": data_id,
            "settings": {"axisX": "213", "axisY": [{"field": "ss", "type": "dsf"}]},
        },
        headers=headers,
    )

    data = response.json()
    assert response.status_code == 201
    assert data.get("title") == "chart fixture for dashboard"
    return data
