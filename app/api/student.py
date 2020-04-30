from datetime import datetime

from flask import jsonify, request, abort
from sqlalchemy import or_

from . import api, read_request_args, check_student_rights
from .. import db
from ..auth import requires_auth
from ..models import Student, Exam, StudentSubscription, Teacher


@api.route('/students/<int:student_id>/exams')
@requires_auth('list:exams')
def get_student_exams(payload, student_id):
    start, end, search = read_request_args()
    student = check_student_rights(payload['sub'])
    students_exams = (Exam.query
                      .join(StudentSubscription)
                      .filter(StudentSubscription.student_id == student.id))
    search_exams = (Exam
                    .text_search(search)
                    .join(StudentSubscription)
                    .filter(StudentSubscription.student_id == student_id))
    search_count = search_exams.count()
    exams_count = students_exams.count()
    start, end = max(start, 0), min(end, search_count)
    exams = Exam.to_list_of_dict(search_exams.slice(start, end),
                                 exclude_fields=['exercises', 'exam_hash',
                                                 'shuffle_exercises'])
    teachers_id = list({exam['author_id'] for exam in exams})
    teachers_names = {teacher.id: teacher.fullname
                      for teacher in (Teacher
                                      .get_query()
                                      .filter(Teacher.id.in_(teachers_id))
                                      .all())}
    for exam in exams:
        exam['teacher'] = teachers_names[exam['author_id']]
    return jsonify({
        'success': True,
        'exams_count': exams_count,
        'search_count': search_count,
        'start': start,
        'end': end,
        'exams': exams
    })


@api.route('/students')
@requires_auth('list:students')
def get_students(payload):
    """Returns a list of students"""
    start, end, search = read_request_args()
    query = Student.text_search(search)
    search_count = query.count()
    students_count = Student.get_query().count()
    start, end = max(start, 0), min(end, search_count)
    students = Student.to_list_of_dict(query.slice(start, end))
    return jsonify({
        'success': True,
        'students_count': students_count,
        'search_count': search_count,
        'start': start,
        'end': end,
        'students': students
    })


@api.route('/students/<int:student_id>')
@requires_auth('view-details:students')
def get_student_by_id(payload, student_id):
    """Returns a single student by its id"""
    student = Student.get_by_id(student_id)
    if student is None:
        abort(404, description='Student not found')
    return jsonify({
        'success': True,
        'student': Student.to_dict(student)
    })


@api.route('/students', methods=['POST'])
@requires_auth('students:create')
def insert_student(payload):
    data = request.get_json()
    if not Student.can_insert(data):
        abort(400, description='Missing student data.')
    username, fullname = data['username'].lower(), data['fullname'].lower()
    student = (Student
               .get_query()
               .filter(or_(
        db.func.lower(Student.username) == username,
        db.func.lower(Student.fullname) == fullname))
               .first())
    if student is not None:
        abort(400, description='The username/fullname is used.')
    student = Student.prepare_insert(data)
    if not student.insert():
        abort(400, description='Error while inserting student data.')
    return jsonify({
        'success': True,
        'student': Student.to_dict(student)
    })


@api.route('/students/<int:student_id>', methods=['PATCH'])
@requires_auth('teachers:edit')
def update_student(payload, student_id):
    student = Student.get_by_id(student_id)
    if student is None:
        abort(404, description='Student not found.')
    data = request.get_json()
    if not Student.can_update(data):
        abort(400, description='Nothing to update.')
    fullname = data['fullname'].lower()
    other_student = (Student
                     .get_query()
                     .filter(db.func.lower(Student.fullname) == fullname)
                     .first())
    if other_student is not None and other_student.id != student_id:
        abort(400, description='The fullname is already used.')
    student.prepare_update(data)
    if not student.update():
        abort(400, description='Error updating student.')
    return jsonify({
        'success': True,
        'student': Student.to_dict(student)
    })


@api.route('/students/<int:student_id>', methods=['DELETE'])
@requires_auth('students:delete')
def delete_student(student_id):
    """
    Mark a student as archived. We don't delete information to preserve data
    integrity.
    """
    student = Student.get_by_id(student_id)
    if student is None:
        abort(404, description='Student not found.')
    student.is_archived = True
    student.dt_archive = datetime.now()
    if not student.update():
        abort(400, description='Error deleting student.')
    return jsonify({
        'success': True,
        'deleted': student_id
    })
