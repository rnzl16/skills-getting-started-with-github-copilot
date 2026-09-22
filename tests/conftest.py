from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


ORIGINAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory app state before each test."""
    app_module.activities.clear()
    app_module.activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app_module.app) as test_client:
        yield test_client
