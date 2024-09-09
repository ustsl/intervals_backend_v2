from tests.conftest import client
from tests.dashboard.fixtures import (create_chart_fixture_for_dashboard,
                                      create_dashboard_fixture)
from tests.user.fixtures import create_user_fuxture, login_user


def test_create_dashboard_chart_relation(
    create_user_fuxture,
    create_dashboard_fixture,
    create_chart_fixture_for_dashboard,
):
    dashboard = create_dashboard_fixture
    chart = create_chart_fixture_for_dashboard

    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}

    response = client.post(
        "/dashboard/chart_relation",
        json={"dashboard_id": dashboard.get("id"), "object_id": chart.get("id")},
        headers=headers,
    )
    data = response.json()
    assert data.get("dashboard_id") == dashboard.get("id")
    assert data.get("object_id") == chart.get("id")
