"""CourseScope API entry point.

Layers (SFDS Section 3):  routes -> services -> repositories -> storage
create_app() wires them together, so tests can build a fresh app each time.
"""
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from repositories.course_repository import InMemoryCourseRepository
from routes.courses import bp as courses_bp
from seed import SEED_COURSES
from services.course_service import CourseService
from services.errors import ServiceError


def create_app(course_repo=None) -> Flask:
    app = Flask(__name__)
    app.json.sort_keys = False

    course_repo = course_repo or InMemoryCourseRepository(SEED_COURSES)
    app.extensions["course_service"] = CourseService(course_repo)

    app.register_blueprint(courses_bp)

    @app.get("/")
    def home():
        return jsonify({"name": "CourseScope API", "status": "running"})

    @app.errorhandler(ServiceError)
    def handle_service_error(err: ServiceError):
        return jsonify({"error": err.message}), err.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(err: HTTPException):
        return jsonify({"error": err.description}), err.code

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
