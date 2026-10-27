"""Seed data used until the database is in place."""
from models import Course

SEED_COURSES = [
    Course(1, "CMPE 131", "Software Engineering I", 3,
           "Software engineering principles, processes, and team projects.",
           ["CMPE 126"]),
    Course(2, "CMPE 125", "Digital Design I", 3,
           "Combinational and sequential logic design.", ["CMPE 50"]),
    Course(3, "CMPE 142", "Operating Systems Design", 3,
           "Processes, scheduling, memory management, and file systems.",
           ["CMPE 102", "CMPE 126"]),
    Course(4, "CMPE 126", "Algorithms and Data Structure Design", 3,
           "Data structures and algorithm design in an object-oriented language.",
           ["CMPE 50"]),
]
