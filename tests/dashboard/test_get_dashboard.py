from tests.conftest import client
from tests.dashboard.fixtures import create_dashboard_fixture, create_chart_fixture_for_dashboard
from tests.user.fixtures import login_user


def test_get_dashboard_list(create_dashboard_fixture):
    data = create_dashboard_fixture
    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}
    response = client.get("/dashboard/", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data.get("total") > 0


def test_get_dashboard_obj(create_dashboard_fixture, create_chart_fixture_for_dashboard):
    dashboard = create_dashboard_fixture
    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}
    response = client.get(f"/dashboard/{dashboard.get("id")}", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data.get("title") == "test dashboard"




