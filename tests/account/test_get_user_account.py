from tests.conftest import client
from tests.user.fixtures import login_user, create_user_fuxture


def test_get_records_not_personal(create_user_fuxture):
    user = login_user()
    headers = {"Authorization": f"Bearer {user}"}
    response = client.get("/account/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("is_active")
