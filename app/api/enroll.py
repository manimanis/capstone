from flask import jsonify, abort, request, redirect, url_for

from . import api, read_request_args, check_student_rights, \
    check_teachers_rights, check_exam_id, check_students_ids
from .. import db
from ..auth import requires_auth
from ..models import Teacher, Exam, StudentSubscription, Student, User, \
    StudentTry


@api.route('/enrolls')
@requires_auth('list:exams')
def list_enrolled_exam(payload):
    """Return the list of exams the authenticated student is enrolled to"""
    username = payload['sub']
    student = check_student_rights(username)
    start, end, search = read_request_args()
    students_exams = Exam.get_by_student_id(student.id)
    search_exams = Exam.text_search_by_student_id(search, student.id)
    search_count = search_exams.count()
    exams_count = students_exams.count()
    start, end = max(start, 0), min(end, search_count)
    exams = Exam.to_list_of_dict(
        search_exams.slice(start, end),
        include_fields=Exam.get_table_columns() + ['teacher'],
        exclude_fields=['exercises', 'is_archived', 'dt_archive',
                        'shuffle_exercises'])
    exams_ids = [exam['id'] for exam in exams]
    count_tries = (StudentTry
                   .num_tries_by_exams_ids(exams_ids, student.id).all())
    students_tries = {exam_id: tries
                      for exam_id, student_id, tries in count_tries}
    for exam in exams:
        exam['num_tries'] = (students_tries[exam['id']]
                             if exam['id'] in students_tries
                             else 0)
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
    students = (Student.get_query()
                .join(StudentSubscription)
                .filter(db.func.not_(Student.is_archived),
                        db.func.not_(StudentSubscription.is_archived),
                        StudentSubscription.exam_id == exam_id)
                .all())
    students = sorted([student.fullname
                       for student in students
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
    enrolls = StudentSubscription.enroll_students(exam_id, students_ids)
    return jsonify({
        'success': True,
        'new_enrolls': enrolls
    })


@api.route('/enrolls/<int:exam_id>', methods=['DELETE'])
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
    deleted_enrolls = StudentSubscription.un_enroll_students(exam_id,
                                                             students_ids)
    return jsonify({
        'success': True,
        'deleted_enrolls': deleted_enrolls
    })
