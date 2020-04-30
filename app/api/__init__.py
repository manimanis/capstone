from flask import Blueprint, request, abort
from ..models import Teacher, Student, Exam

api = Blueprint('api', __name__)


def read_request_args():
    """
    Read common request arguments.
    Return the starting row and the ending row and the search term.
    """
    start = request.args.get('start', 0, type=int)
    end = request.args.get('end', start + 10, type=int)
    search = request.args.get('search', '')
    start, end = min(start, end), max(start, end)
    return start, end, search


def check_teachers_rights(username):
    """Check if 'username' is really a teacher"""
    teacher_obj = Teacher.get_by_username(username)
    if teacher_obj is None or not teacher_obj.is_teacher():
        abort(403,
              description='You are not authorized to access this resource.')
    return teacher_obj


def check_student_rights(username):
    """Check if 'username' is really a student"""
    student_obj = Student.get_by_username(username)
    if student_obj is None or not student_obj.is_student():
        abort(403, description='You are not authorized to access this '
                               'resource.')
    return student_obj


def check_exam_id(exam_id):
    """Checks that the 'exam_id' is valid"""
    exam = Exam.get_by_id(exam_id)
    if exam is None:
        abort(404, description='Exam not found.')
    return exam


def check_students_ids(students_ids):
    """Checks that the 'students_ids' is a list of integers"""
    if type(students_ids) != list \
            or any(type(student_id) != int for student_id in students_ids):
        abort(400, description='Provide a list of students ids.')
    # remove duplicates
    return list(set(students_ids))


@api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, accept, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,POST,PATCH,DELETE,OPTIONS')
    return response


from . import test, user, teacher, student, exam, enroll, tries
