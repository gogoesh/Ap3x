"""HTTP layer for courses. Routes only parse requests and shape responses;
all rules live in the service layer."""
from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("courses", __name__, url_prefix="/api/courses")


def _courses():
    return current_app.extensions["course_service"]


@bp.get("")
def list_courses():
    return jsonify([c.to_dict() for c in _courses().list_courses()])


@bp.get("/search")
def search_courses():
    results = _courses().search(request.args.get("q", ""))
    return jsonify([c.to_dict() for c in results])


@bp.get("/<int:course_id>")
def get_course(course_id: int):
    return jsonify(_courses().get_course(course_id).to_dict())