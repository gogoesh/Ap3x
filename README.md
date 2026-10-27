# CourseScope

CourseScope is a course-review platform for SJSU students: search courses, read reviews,
and post reviews of courses you've taken.

This repository currently contains the **backend API** (Python / Flask). The frontend comes later.

## Architecture

The backend follows the layered design in our SFDS (Section 3) and SAD. Each layer only
talks to the one below it.

```
HTTP request
    |
routes/         Flask blueprints: parse the request, return JSON (no business rules)
    |
services/       Business rules: validation, ownership checks, review lifecycle
    |
repositories/   Data access: the only layer that knows how data is stored
    |
storage         In-memory for now; SQLite next (no changes needed above this layer)
```

| Folder / file | Contents |
|---|---|
| `backend/app.py` | `create_app()` wires repositories, services, and routes together |
| `backend/models.py` | Dataclasses for User, Instructor, Course, Review (SFDS 7.1) |
| `backend/seed.py` | Seed course data used until the database is added |
| `backend/routes/` | `courses.py`, `reviews.py` |
| `backend/services/` | `course_service.py`, `review_service.py`, `errors.py` |
| `backend/repositories/` | `course_repository.py`, `review_repository.py` |
| `backend/tests/` | pytest suite for endpoints and validation |

## Run locally

Requires Python 3.14 (pinned in `.python-version`).

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
python app.py                  # http://127.0.0.1:5000
```

## Run tests

```bash
cd backend
python -m pytest -v
```

## API

| Method | Path | Description |
|---|---|---|
| GET | `/` | API status |
| GET | `/api/courses` | List all courses |
| GET | `/api/courses/search?q=...` | Search by code, title, or description |
| GET | `/api/courses/<id>` | Course details |
| GET | `/api/courses/<id>/reviews` | Published reviews for a course |
| POST | `/api/courses/<id>/reviews` | Create a review (needs `X-User-Id`) |
| GET | `/api/reviews/<id>` | Single review |
| PATCH | `/api/reviews/<id>` | Update your own review (needs `X-User-Id`) |
| DELETE | `/api/reviews/<id>` | Delete your own review (needs `X-User-Id`) |

`X-User-Id` is a **temporary placeholder** for authentication. Real SJSU-verified login
is planned after the code review.

Example review body:

```json
{"rating": 4, "text": "Great project-based class.", "term": "Fall 2025",
 "grade": "A-", "difficulty": 3, "workload": 4}
```

- `rating` and `text` are required when creating a review.
- `rating`, `difficulty`, and `workload` are integers from 1 to 5.
- `PATCH` accepts any subset of these fields.
- Unknown fields (for example `author_id`) are rejected.

Errors always return `{"error": "message"}` with one of these status codes:

| Status | Meaning |
|---|---|
| 400 | Invalid input |
| 401 | Missing `X-User-Id` |
| 403 | Not the review's author |
| 404 | Course or review not found |

## Not yet implemented (planned)

SQLite persistence, real authentication and SJSU verification, review reporting and
moderation, instructor endpoints, rating averages, deployment, and the frontend.
```

