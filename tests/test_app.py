import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (nothing to set up for in-memory data)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_prevent_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Act: Try duplicate signup
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

def test_unregister_participant():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]
    # Act: Try to remove again
    response2 = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response2.status_code == 404
    assert "not signed up" in response2.json()["detail"]
