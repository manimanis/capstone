from datetime import datetime, date

from flask import abort, jsonify
from . import api, read_request_args
from ..auth import requires_auth
from ..models import User, StudentTry, Exam


@api.route('/tries/<int:exam_id>')
@requires_auth('try-resolve:exams')
def get_exam_tries(payload, exam_id):
    """Return the results in the exam having the <exam_id>."""
    username = payload['sub']
    user = User.get_by_username(username)
    if user is None:
        abort(403, description='Not authorized to view exam results.')
    start, end, search = read_request_args()
    base_query = (StudentTry.query
                  .filter(StudentTry.exam_id == exam_id)
                  .order_by(StudentTry.dt_try.desc()))
    tries_count = base_query.count()
    start, end = max(start, 0), min(end, tries_count)
    tries = StudentTry.to_list_of_dict(
        base_query.slice(start, end),
        include_fields=['current_state', 'description', 'dt_try',
                        'exam_duration', 'exam_hash', 'teacher_fullname',
                        'teacher_username', 'title', 'student_score',
                        'total_score'])
    return jsonify({
        'success': True,
        'start': start,
        'end': end,
        'tries_count': tries_count,
        'tries': tries
    })


@api.route('/tries/<int:exam_id>', methods=['POST'])
@requires_auth('try-resolve:exams')
def initiate_exam(payload, exam_id):
    """Initiate a new try for the <exam_id>, the user will have the allocated
    time to return the exam answers"""
    username = payload['sub']
    user = User.get_by_username(username)
    if user is None:
        abort(403, description='Not authorized to try exams.')
    # Students cannot pass archived exams
    exam = Exam.get_by_id(exam_id)
    if exam is None:
        abort(404, description='Exam not found.')
    # Check if the exam is available for tries at this time
    if not (exam.from_date <= datetime.now() <= exam.to_date):
        abort(400, description=f'Exam is available from {exam.from_date} '
                               f'to {exam.to_date()}')
    teacher = exam.teacher
    # Find all the tries made by this student to this exam
    student_tries = (StudentTry.query
                     .filter(StudentTry.exam_id == exam.id,
                             StudentTry.teacher_id == teacher.id,
                             StudentTry.student_id == user.id)
                     .order_by(StudentTry.dt_expiration.desc()))
    # Is there any exam session opened at this time
    student_try = (student_tries
                   .filter(StudentTry.dt_expiration >= datetime.now())
                   .first())
    if student_try is None:
        # The student cannot make more then <exam.max_retries> count
        tries_count = student_tries.count()
        if tries_count + 1 > exam.max_retries:
            abort(400, description='No retries are available for this exam.')
        # Everything is ok create a new try/retry
        student_try = StudentTry()
        student_try.create_new_try(user, teacher, exam)
        if not student_try.insert():
            abort(400, description='Cannot start an exam.')
    return jsonify({
        'success': True,
        'exam': exam.stripped_exercises(),
        'try': StudentTry.to_dict(student_try, exclude_fields=['exercises'])
    })


@api.route('/tries/<int:exam_id>', methods=['PATCH'])
@requires_auth('try-resolve:exams')
def send_exam_answers(payload, exam_id):
    """Send the answers"""
    pass
