"""Course rules: searching and looking up courses."""
from models import Course
from services.errors import NotFoundError, ValidationError

MAX_QUERY_LENGTH = 100


class CourseService:
    def __init__(self, course_repo):
        self.courses = course_repo

    def list_courses(self) -> list[Course]:
        return self.courses.list_all()

    def get_course(self, course_id: int) -> Course:
        course = self.courses.get(course_id)
        if course is None:
            raise NotFoundError("Course not found")
        return course

    def search(self, query: str) -> list[Course]:
        query = (query or "").strip()
        if not query:
            raise ValidationError("Search query 'q' is required")
        if len(query) > MAX_QUERY_LENGTH:
            raise ValidationError(f"Search query must be at most {MAX_QUERY_LENGTH} characters")
        return self.courses.search(query)