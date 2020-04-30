import json
import time
from datetime import datetime, date, timedelta

from flask import abort, jsonify, request
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
    elif student_try.current_state not in [StudentTry.SAVE, StudentTry.STARTED]:
        abort(400, description='You have either completed the exam or it is '
                               'expired.')
    exam_try = StudentTry.to_dict(student_try, exclude_fields=['exercises'])
    answers_history = json.loads(exam_try['answers'])
    if len(answers_history) > 0:
        exam_try['answers'] = answers_history[-1]['answers']
    else:
        exam_try['answers'] = []
    return jsonify({
        'success': True,
        'exam': exam.stripped_exercises(),
        'try': exam_try
    })


@api.route('/tries/<int:try_id>', methods=['PATCH'])
@requires_auth('try-resolve:exams')
def send_exam_answers(payload, try_id):
    """Send the answers"""
    current_time = datetime.now()
    username = payload['sub']
    # only users can send answers
    user = User.get_by_username(username)
    if user is None:
        abort(403, description='Not authorized to send answers for this '
                               'exams.')
    # only the user with the correct student_id can send answers
    student_try = StudentTry.get_by_id(try_id)
    if student_try.student_id != user.id:
        abort(403, description="You cannot answer someone else exam.")
    # cannot send answers for an expired or completed exam
    if student_try.current_state not in [StudentTry.SAVE, StudentTry.STARTED]:
        abort(403, description='Cannot answer expired or completed exam.')
    # grab essential data: exam_id, teacher_id
    data = request.get_json()
    exam_id = data.get('exam_id', 0)
    teacher_id = data.get('teacher_id', 0)
    current_state = data.get('current_state', -1)
    answers = data.get('answers', [])
    # must provide exact information about exam_id and teacher_id
    if student_try.exam_id != exam_id or student_try.teacher_id != teacher_id:
        abort(400, description='Make sure you are sending the answers for the '
                               'right exam.')
    # must provide correct state: either save answers or tell us that you wish
    # to end the exam
    if (current_state != StudentTry.SAVE
            and current_state != StudentTry.COMPLETED):
        abort(400, description='Nothing could be done to the request.')
    # We tolerate only 120s after the sending delay
    # but we save the students answers
    expired_alert = (current_time > (student_try.dt_expiration +
                                     timedelta(seconds=120)))
    answers_history = json.loads(student_try.answers)
    if len(answers_history) > 0:
        # we will save the answers only if it is different from the last one
        last_answer = answers_history[-1]
        new_answer = last_answer['answers'] != answers
    else:
        new_answer = True
    # always save the answers if the exam expires or if the exam is marked
    # as completed
    if new_answer or expired_alert or current_state == StudentTry.COMPLETED:
        answers_history.append({'date': str(current_time), 'answers': answers})
        student_try.answers = json.dumps(answers_history)
        student_try.current_state = (
            StudentTry.EXPIRED
            if expired_alert and current_state != StudentTry.COMPLETED
            else StudentTry.COMPLETED if current_state == StudentTry.COMPLETED
            else StudentTry.SAVE)
        if not student_try.update():
            abort(400, description='Could not update answers.')
    return jsonify({
        'success': True,
        'expired_alert': expired_alert
    })




