from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(app_module.activities)
    app_module.activities = deepcopy(original)
    yield
    app_module.activities = deepcopy(original)


client = TestClient(app_module.app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = "Chess%20Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/unregister?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_returns_error_for_unknown_student():
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = "Chess%20Club"
    email = "unknown@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/unregister?email={email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
