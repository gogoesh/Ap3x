"""CourseScope API entry point.

Layers (SFDS Section 3):  routes -> services -> repositories -> storage
create_app() wires them together, so tests can build a fresh app each time.
"""
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from repositories.course_repository import InMemoryCourseRepository
from repositories.review_repository import InMemoryReviewRepository
from routes.courses import bp as courses_bp
from routes.reviews import bp as reviews_bp
from seed import SEED_COURSES
from services.course_service import CourseService
from services.errors import ServiceError
from services.review_service import ReviewService


def create_app(course_repo=None, review_repo=None) -> Flask:
    app = Flask(__name__)
    app.json.sort_keys = False

    course_repo = course_repo or InMemoryCourseRepository(SEED_COURSES)
    review_repo = review_repo or InMemoryReviewRepository()

    course_service = CourseService(course_repo)
    app.extensions["course_service"] = course_service
    app.extensions["review_service"] = ReviewService(review_repo, course_service)

    app.register_blueprint(courses_bp)
    app.register_blueprint(reviews_bp)

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