from tests.conftest import client
from tests.chart.fixtures import create_chart_fixture
from tests.user.fixtures import login_user


def test_get_chart_list(create_chart_fixture):
    data = create_chart_fixture

    user = login_user()

    headers = {"Authorization": f"Bearer {user}"}
    response = client.get("/chart/", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data.get("total") > 0


def test_get_chart_obj(create_chart_fixture):
    data = create_chart_fixture
    print(data.get("id"))
    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}
    response = client.get(f"/chart/{data.get("id")}", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data.get("title") == "chart fixture 1"
