import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 302)
    # Should redirect to /static/index.html
    assert "/static/index.html" in str(response.url)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email for test
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Ensure not already registered
    client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    # Signup
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json().get("message", "")
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response2.status_code == 400
    # Unregister
    response3 = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    assert response3.status_code == 200
    assert f"Removed {test_email}" in response3.json().get("message", "")
    # Unregister again should fail
    response4 = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    assert response4.status_code == 404
