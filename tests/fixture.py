import random

from app import db
from app.models import Teacher, Student, User, Exam, StudentSubscription
from tests.sample_exams import generate_random_exam
from tests.sample_users import generate_random_users


def create_fixture_users(count=10):
    print(f'Inserting {count} users...')
    users_dict = generate_random_users(count, ['teacher', 'student'])
    users = []
    for user_dict in users_dict:
        if user_dict['role'] == 'teacher':
            cls = Teacher
        else:
            cls = Student
        del user_dict['role']
        users.append(cls(**user_dict, is_archived=False))
    if User.persist_changes({'insert': users}):
        print(f'The {len(users)} users were added...')
    else:
        print(f'Cannot insert users...')


def create_fixture_exams(count=10):
    print(f'Inserting {count} exams...')
    teachers = Teacher.query.all()
    exams = [Exam(**generate_random_exam(random.choice(teachers).id))
             for _ in range(count)]
    if Exam.persist_changes({'insert': exams}):
        print(f'The {len(exams)} exams were added...')
    else:
        print(f'Cannot insert exams.')


def create_fixture_subscription():
    print(f'Inserting student enrolls.')
    exams_ids = [exam.id for exam in Exam.query.all()]
    students_id = [student.id for student in Student.query.all()]
    exams_enrolls = []
    for student_id in students_id:
        exams_copy = exams_ids.copy()
        exams_picks = random.randint(1, max(2, len(exams_ids)))
        for _ in range(exams_picks):
            pick_exam_number = random.randint(0, len(exams_copy) - 1)
            exams_enrolls.append(
                StudentSubscription(
                    exam_id=exams_copy[pick_exam_number],
                    student_id=student_id))
            del exams_copy[pick_exam_number]
    if StudentSubscription.persist_changes({'insert': exams_enrolls}):
        print(f'The {len(exams_enrolls)} exams enrolls were added...')
    else:
        print(f'Cannot insert exams enrolls.')


def create_fixture():
    db.drop_all()
    db.create_all()
    print('Generating fixture data...')
    create_fixture_users()
    create_fixture_exams()
    create_fixture_subscription()
