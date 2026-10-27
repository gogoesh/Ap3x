"""Review rules: validation, ownership, and the review lifecycle."""
from typing import Optional

from models import Review
from services.errors import NotFoundError, UnauthorizedError, ValidationError

MAX_TEXT_LENGTH = 2000
SCORED_FIELDS = ("rating", "difficulty", "workload")      # all 1-5
OPTIONAL_TEXT_FIELDS = ("term", "grade")
EDITABLE_FIELDS = SCORED_FIELDS + OPTIONAL_TEXT_FIELDS + ("text", "instructor_id")


class ReviewService:
    def __init__(self, review_repo, course_service):
        self.reviews = review_repo
        self.course_service = course_service

    # ----- queries -------------------------------------------------------
    def list_for_course(self, course_id: int) -> list[Review]:
        self.course_service.get_course(course_id)   # 404 if course missing
        return self.reviews.list_for_course(course_id)

    def get_review(self, review_id: int) -> Review:
        review = self.reviews.get(review_id)
        if review is None or review.status == "removed":
            raise NotFoundError("Review not found")
        return review

    # ----- commands ------------------------------------------------------
    def create_review(self, course_id: int, data: Optional[dict],
                      author_id: Optional[int]) -> Review:
        self._require_author(author_id)
        self.course_service.get_course(course_id)   # 404 if course missing
        data = self._validate(data, partial=False)

        review = Review(
            id=self.reviews.next_id(),
            course_id=course_id,
            author_id=author_id,
            rating=data["rating"],
            text=data["text"],
            instructor_id=data.get("instructor_id"),
            term=data.get("term"),
            grade=data.get("grade"),
            difficulty=data.get("difficulty"),
            workload=data.get("workload"),
        )
        return self.reviews.add(review)

    # ----- helpers -------------------------------------------------------
    @staticmethod
    def _require_author(author_id: Optional[int]) -> None:
        # Placeholder for real authentication (deferred until after the
        # code review). For now the caller identifies itself with the
        # X-User-Id header.
        if author_id is None:
            raise UnauthorizedError("X-User-Id header required")

    @staticmethod
    def _validate(data: Optional[dict], partial: bool) -> dict:
        if not isinstance(data, dict) or not data:
            raise ValidationError("Review data required")

        unknown = set(data) - set(EDITABLE_FIELDS)
        if unknown:
            raise ValidationError(f"Unknown field(s): {', '.join(sorted(unknown))}")

        if not partial:
            for required in ("rating", "text"):
                if required not in data:
                    raise ValidationError(f"'{required}' is required")

        clean: dict = {}
        for key in SCORED_FIELDS:
            if key in data and data[key] is not None:
                value = data[key]
                if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5:
                    raise ValidationError(f"'{key}' must be an integer from 1 to 5")
                clean[key] = value

        if "text" in data:
            text = data["text"]
            if not isinstance(text, str) or not text.strip():
                raise ValidationError("'text' must be a non-empty string")
            if len(text) > MAX_TEXT_LENGTH:
                raise ValidationError(f"'text' must be at most {MAX_TEXT_LENGTH} characters")
            clean["text"] = text.strip()

        for key in OPTIONAL_TEXT_FIELDS:
            if key in data and data[key] is not None:
                if not isinstance(data[key], str):
                    raise ValidationError(f"'{key}' must be a string")
                clean[key] = data[key].strip()

        instructor_id = data.get("instructor_id")
        if instructor_id is not None:
            if isinstance(instructor_id, bool) or not isinstance(instructor_id, int):
                raise ValidationError("'instructor_id' must be an integer")
            clean["instructor_id"] = instructor_id

        return clean