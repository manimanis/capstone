from flask import jsonify, abort, request, redirect

from . import api, read_request_args, check_student_rights, \
    check_teachers_rights
from .. import db
from ..auth import requires_auth
from ..models import Teacher, Exam, StudentSubscription, Student, User


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


@api.route('/enrolls')
@requires_auth('list:exams')
def list_enrolled_exam(payload):
    """Return the list of exams the student is enrolled to"""
    username = payload['sub']
    student = check_student_rights(username)
    start, end, search = read_request_args()
    students_exams = Exam.get_by_student_id(student.id)
    search_exams = Exam.text_search_by_student_id(search, student.id)
    search_count = search_exams.count()
    exams_count = students_exams.count()
    start, end = max(start, 0), min(end, search_count)
    exams = Exam.to_list_of_dict(search_exams.slice(start, end))
    return jsonify({
        'success': True,
        'exams_count': exams_count,
        'search_count': search_count,
        'start': start,
        'end': end,
        'exams': exams
    })


@api.route('/enrolls/<int:exam_id>')
@requires_auth('list:students')
def list_enrolled_students(payload, exam_id):
    """Return the list of students enrolled to one exam."""
    teacher = check_teachers_rights(payload['sub'])
    exam = Exam.get_by_id(exam_id)
    if exam is None:
        abort(404, description='Exam not found.')
    if exam.author_id != teacher.id:
        abort(403, description="Cannot view others teachers enrolled "
                               "students.")
    students = sorted([student.fullname
                       for student in exam.students
                       if not student.is_archived])
    return jsonify({
        'success': True,
        'students': students
    })


@api.route('/enrolls/<int:exam_id>', methods=['POST'])
@requires_auth('enroll:exams')
def enroll_students_to_exam(payload, exam_id):
    """
    When invoked by teachers: Enrolls student list to an 'exam_id'
    When invoked by students: Enrolls the student to the 'exam_id'
    """
    username = payload['sub']
    user = User.get_by_username(username)
    if user is None:
        abort(403, description='Not authorized to enroll to exams.')
    students_ids = request.get_json()
    exam = check_exam_id(exam_id)
    students_ids = check_students_ids(students_ids)
    if user.is_teacher():
        if exam.author_id != user.id:
            abort(403,
                  description='Cannot enroll students to others teachers '
                              'exams.')
        if len(students_ids) == 0:
            abort(400, description='No students are provided to enroll.')
        # remove duplications
        students_ids = list(set(students_ids))
        # check if all the students ids are stored in the database
        Student.check_students_ids(students_ids)
    elif user.is_student():
        if len(students_ids) != 0:
            abort(403, description='Cannot enroll others students.')
        # we will enroll only a unique student
        students_ids = [user.id]
    else:
        abort(403, description='You are not allowed to enroll.')
    if not StudentSubscription.enroll_students(exam_id, students_ids):
        abort(400, description='Cannot persist new enrolls.')
    if user.is_teacher():
        return redirect(f'/enrolls/{exam_id}')
    elif user.is_student():
        start, end, search = read_request_args()
        return redirect(f'/enrolls?search={search}&start={start}&end={end}')


@api.route('/enrolls/<int:exam_id>', methods=['PATCH'])
@requires_auth('enroll:exams')
def un_enroll_students_to_exam(payload, exam_id):
    """
    When invoked by teachers: Un-enrolls student list to an 'exam_id'
    When invoked by students: Un-enrolls the student to the 'exam_id'
    """
    username = payload['sub']
    user = User.get_by_username(username)
    if user is None:
        abort(403, description='Not authorized to unenroll to exams.')
    students_ids = request.get_json()
    exam = check_exam_id(exam_id)
    students_ids = check_students_ids(students_ids)
    if user.is_teacher():
        if exam.author_id != user.id:
            abort(403,
                  description='Cannot un-enroll students to others teachers '
                              'exams.')
        if len(students_ids) == 0:
            abort(400, description='No students are provided to un-enroll.')
        # remove duplications
        students_ids = list(set(students_ids))
    elif user.is_student():
        if len(students_ids) != 0:
            abort(403, description='Cannot enroll others students.')
        # we will un-enroll only a unique student
        students_ids = [user.id]
    else:
        abort(403, description='You are not allowed to un-enroll.')
    # Check if all of the students_ids are enrolled to this exam_id
    if (StudentSubscription
            .enrolled_count_in_students_ids(exam_id, students_ids)
            != len(students_ids)):
        abort(400, description='Not all of the students are enrolled.')
    if not StudentSubscription.un_enroll_students(exam_id, students_ids):
        abort(400, description='Cannot persist un-enrolls.')
    if user.is_teacher():
        return redirect(f'/enrolls/{exam_id}')
    elif user.is_student():
        start, end, search = read_request_args()
        return redirect(f'/enrolls?search={search}&start={start}&end={end}')
