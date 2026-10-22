import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import get_current_user


@pytest.fixture
def client():
    # Override the get_current_user dependency to bypass authentication for testing
    app.dependency_overrides[get_current_user] = lambda: {"id": 1}

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        # Remove the dependency override after the test
        app.dependency_overrides.pop(get_current_user, None)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Running"}


def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "message": "API is running successfully"}


def test_create_customer_without_company_name(client):
    response = client.post(
        "/api/v1/customers",
        json={
            "contact_person": "Ghulam Murtaza",
            "email": "puregoldendemolition@gmail.com",
        },
    )
    assert response.status_code == 422


def test_create_customer_with_invalid_email(client):
    response = client.post(
        "/api/v1/customers",
        json={
            "company_name": "Pure Golden Wrecking & Demolition Works LLC",
            "contact_person": "Ghulam Murtaza",
            "email": "invalid-email",
        },
    )
    assert response.status_code == 422
