"""HTTP layer for reviews."""
from typing import Optional

from flask import Blueprint, current_app, jsonify, request

from services.errors import ValidationError

bp = Blueprint("reviews", __name__, url_prefix="/api")


def _reviews():
    return current_app.extensions["review_service"]


def _current_user_id() -> Optional[int]:
    """Temporary stand-in for authentication: read X-User-Id.
    Replace with real session/token auth after the code review."""
    raw = request.headers.get("X-User-Id")
    if raw is None:
        return None
    if not raw.isdigit():
        raise ValidationError("X-User-Id must be a positive integer")
    return int(raw)


def _json_body() -> Optional[dict]:
    return request.get_json(silent=True)


@bp.get("/courses/<int:course_id>/reviews")
def list_reviews(course_id: int):
    return jsonify([r.to_dict() for r in _reviews().list_for_course(course_id)])


@bp.post("/courses/<int:course_id>/reviews")
def create_review(course_id: int):
    review = _reviews().create_review(course_id, _json_body(), _current_user_id())
    return jsonify(review.to_dict()), 201


@bp.get("/reviews/<int:review_id>")
def get_review(review_id: int):
    return jsonify(_reviews().get_review(review_id).to_dict())