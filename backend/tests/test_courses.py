"""Course endpoint tests (maps to SFDS T-01 and T-12)."""


def test_home_reports_running(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.get_json()["status"] == "running"


def test_list_courses_returns_seed_data(client):
    res = client.get("/api/courses")
    assert res.status_code == 200
    codes = [c["code"] for c in res.get_json()]
    assert "CMPE 131" in codes


def test_search_by_code(client):                      # T-01
    res = client.get("/api/courses/search?q=cmpe 131")
    assert res.status_code == 200
    assert [c["code"] for c in res.get_json()] == ["CMPE 131"]


def test_search_by_title_keyword(client):
    res = client.get("/api/courses/search?q=operating")
    assert [c["code"] for c in res.get_json()] == ["CMPE 142"]


def test_search_with_no_matches_returns_empty_list(client):
    res = client.get("/api/courses/search?q=underwater basket weaving")
    assert res.status_code == 200
    assert res.get_json() == []


def test_search_requires_query(client):
    res = client.get("/api/courses/search")
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_get_course_by_id(client):                    # T-12
    res = client.get("/api/courses/1")
    assert res.status_code == 200
    assert res.get_json()["code"] == "CMPE 131"


def test_get_unknown_course_returns_404(client):
    res = client.get("/api/courses/999")
    assert res.status_code == 404
    assert res.get_json() == {"error": "Course not found"}