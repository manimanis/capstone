from . import auth0_methods
from . import sample_exams
from . import sample_users
from . import fixture

TEACHER_PERMISSIONS = [
    "archive:exams",
    "create:exams",
    "edit:exams",
    "enroll:exams",
    "list:exams",
    "list:students",
    "try-resolve:exams",
    "view-details:exams",
    "view-details:students"
]
STUDENT_PERMISSIONS = [
    "enroll:exams",
    "list:exams",
    "list:teachers",
    "try-resolve:exams",
    "view-details:teachers"
]

