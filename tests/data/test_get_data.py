from tests.conftest import client
from tests.data.fixtures import create_data_fixture
from tests.user.fixtures import login_user


def test_get_data_list(create_data_fixture):
    data = create_data_fixture

    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}
    response = client.get("/data/", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data.get("total") > 0


def test_get_data_obj(create_data_fixture):
    data = create_data_fixture
    print(data.get("id"))
    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}
    response = client.get(f"/data/{data.get("id")}", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data.get("title") == "data fixtures"
