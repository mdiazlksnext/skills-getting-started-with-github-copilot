import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# AAA: Arrange-Act-Assert pattern in all tests

def test_get_activities():
    # Arrange
    # (No setup needed, just call endpoint)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_signup_for_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Cleanup: remove user if present
    client.delete(f"/activities/{activity}/signup?email={email}")

def test_signup_for_activity_already_registered():
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/signup?email={email}")

def test_signup_for_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser3@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_from_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser4@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

def test_unregister_from_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser5@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_from_activity_not_registered():
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]
