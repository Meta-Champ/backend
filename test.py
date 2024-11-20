from main import application
from fastapi.testclient import TestClient

client = TestClient(application)


def test_authorization() -> None:
    response_start = client.post(
        '/api/auth/login', 
        json={
            'username': 'metaadmin',
            'password': 'metapass'
        }
    )

    data = response_start.json()

    assert response_start.status_code == 200
    assert 'access_token' in data
    assert 'refresh_token' in data
