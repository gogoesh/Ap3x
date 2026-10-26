"""Domain models for CourseScope.
Plain dataclasses keep the domain independent of Flask and of the storage technology.
The fields follow SFDS Section 7.1 (Database Schema)."""

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Optional

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

@dataclass
class User:
    id: int
    email: str
    role: str = "student"               # Student or moderator
    verified: bool = False              # SJSU Verification status

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Instructor:
    id: int
    name: str
    aliases: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Course:
    id: int
    code: str
    title: str
    units: str
    description: str = ""
    prerequisites: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Review:
    id: int
    course_id: int
    author_id: int
    rating: int
    text: str

    instructor_id: Optional[int] = None
    term: Optional[int] = None              # e.g. "Fall 2026"
    grade: Optional[int] = None             # e.g. "B+"
    difficulty: Optional[int] = None        # 1-5
    workload: Optional[int] = None          # 1-5
    status: str = "published"               # published, hidden or removed
    created_at: str = field(default_factory=utc_now)
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)