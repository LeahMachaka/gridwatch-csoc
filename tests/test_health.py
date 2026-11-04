import pytest


@pytest.mark.django_db
def test_health_returns_status_key(client):
    response = client.get("/health/")

    assert response.headers["Content-Type"] == "application/json"
    assert "status" in response.json()
