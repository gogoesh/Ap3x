"""Course repository: the only code that knows where courses are stored.

Currently in-memory. To move to SQLite or some other database, keep these method names and
change only the bodies; services and routes do not need to change.
"""

from typing import Optional
from models import Course


class InMemoryCourseRepository:
    def __init__(self, courses: Optional[list[Course]] = None):
        self._courses: dict[int, Course] = {c.id: c for c in (courses or [])}

    def list_all(self) -> list[Course]:
        return sorted(self._courses.values(), key=lambda c: c.code)

    def get(self, course_id: int) -> Optional[Course]:
        return self._courses.get(course_id)

    def search(self, query: str) -> list[Course]:
        q = query.strip().lower()
        return [
            c for c in self.list_all()
            if q in c.code.lower() or q in c.title.lower()
               or q in c.description.lower()
        ]
