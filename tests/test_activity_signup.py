import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import app, activities

client = TestClient(app)


def reset_activities():
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    activities["Programming Class"]["participants"] = [
        "emma@mergington.edu",
        "sophia@mergington.edu",
    ]


def test_duplicate_signup_is_rejected():
    reset_activities()

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_removes_participant_from_activity():
    reset_activities()

    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "daniel@mergington.edu"},
    )

    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
