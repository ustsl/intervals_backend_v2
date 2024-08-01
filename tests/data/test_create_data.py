from tests.conftest import client


def test_failed_create_data_with_old_token():

    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYTk0ZGVmOS1lYWZkLTRkYzEtYmY5My05ZmQ0NjZjZTRiYWUiLCJhdWQiOlsiZmFzdGFwaS11c2VyczphdXRoIl0sImV4cCI6MTcyMTk5NTI2MH0.jgo94ywbPZqwNBFWOGaWdGM3G63sp3m_QuYovT9YVQA"
    }

    response = client.post(
        "/data",
        json={"title": "data", "container": {"data": "data"}},
        headers=headers,
    )
    assert response.status_code == 401
