import uuid

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant():
    email = f"copilot-remove-{uuid.uuid4().hex[:8]}@example.com"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected():
    email = f"copilot-duplicate-{uuid.uuid4().hex[:8]}@example.com"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()
