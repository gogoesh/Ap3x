"""Review repository (in-memory for now)."""
from itertools import count
from typing import Optional

from models import Review


class InMemoryReviewRepository:
    def __init__(self):
        self._reviews: dict[int, Review] = {}
        # A counter (not len()+1) so IDs never repeat after a delete.
        self._next_id = count(1)

    def next_id(self) -> int:
        return next(self._next_id)

    def add(self, review: Review) -> Review:
        self._reviews[review.id] = review
        return review

    def get(self, review_id: int) -> Optional[Review]:
        return self._reviews.get(review_id)

    def list_for_course(self, course_id: int, status: str = "published") -> list[Review]:
        return [
            r for r in self._reviews.values()
            if r.course_id == course_id and r.status == status
        ]

    def update(self, review: Review) -> Review:
        self._reviews[review.id] = review
        return review

    def delete(self, review_id: int) -> None:
        self._reviews.pop(review_id, None)