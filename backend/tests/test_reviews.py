"""Review endpoint tests: create/read, validation, ownership."""
import pytest


def create(client, payload, headers, course_id=1):
    return client.post(f"/api/courses/{course_id}/reviews", json=payload, headers=headers)


# ----- create / read --------------------------------------------------------
def test_create_and_list_review(client, review_payload, author_headers):
    res = create(client, review_payload, author_headers)
    assert res.status_code == 201
    body = res.get_json()
    assert body["id"] == 1
    assert body["author_id"] == 1
    assert body["status"] == "published"

    listed = client.get("/api/courses/1/reviews").get_json()
    assert [r["id"] for r in listed] == [1]


def test_reviews_are_scoped_to_their_course(client, review_payload, author_headers):
    create(client, review_payload, author_headers, course_id=1)
    assert client.get("/api/courses/2/reviews").get_json() == []


def test_review_for_unknown_course_returns_404(client, review_payload, author_headers):
    assert create(client, review_payload, author_headers, course_id=999).status_code == 404


# ----- validation -----------------------------------------------------------
def test_create_requires_author_header(client, review_payload):
    assert create(client, review_payload, {}).status_code == 401


@pytest.mark.parametrize("payload, message", [
    (None, "Review data required"),
    ({"text": "No rating"}, "'rating' is required"),
    ({"rating": 4}, "'text' is required"),
    ({"rating": 6, "text": "x"}, "'rating' must be an integer from 1 to 5"),
    ({"rating": "5", "text": "x"}, "'rating' must be an integer from 1 to 5"),
    ({"rating": 3, "text": "   "}, "'text' must be a non-empty string"),
    ({"rating": 3, "text": "x", "difficulty": 0}, "'difficulty' must be an integer from 1 to 5"),
    ({"rating": 3, "text": "x", "author_id": 99}, "Unknown field(s): author_id"),
])
def test_create_rejects_bad_input(client, author_headers, payload, message):
    res = create(client, payload, author_headers)
    assert res.status_code == 400
    assert res.get_json()["error"] == message