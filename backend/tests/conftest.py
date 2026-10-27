import os
import sys

import pytest

# Make backend/ importable when running `pytest` from the backend folder.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402


@pytest.fixture
def client():
    app = create_app()          # fresh in-memory data for every test
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture
def review_payload():
    return {"rating": 4, "text": "Great project-based class.",
            "term": "Fall 2025", "grade": "A-", "difficulty": 3, "workload": 4}


@pytest.fixture
def author_headers():
    return {"X-User-Id": "1"}