from datetime import datetime

from flask import jsonify, request, abort
from sqlalchemy import or_

from . import api, read_request_args
from .. import db
from ..auth import requires_auth
from ..models import Teacher


@api.route('/teachers')
@requires_auth('list:teachers')
def get_teachers(payload):
    """Returns a list of teachers"""
    start, end, search = read_request_args()
    query = Teacher.text_search(search)
    search_count = query.count()
    teachers_count = Teacher.get_query().count()
    start, end = max(start, 0), min(end, search_count)
    teachers = Teacher.to_list_of_dict(query.slice(start, end))
    return jsonify({
        'success': True,
        'teachers_count': teachers_count,
        'search_count': search_count,
        'start': start,
        'end': end,
        'teachers': teachers
    })


@api.route('/teachers/<int:teacher_id>')
@requires_auth('view-details:teachers')
def get_teacher_by_id(payload, teacher_id):
    """Returns a single teacher by its id"""
    teacher = Teacher.get_by_id(teacher_id)
    if teacher is None:
        abort(404, description='Teacher not found')
    return jsonify({
        'success': True,
        'teacher': Teacher.to_dict(teacher)
    })


@api.route('/teachers', methods=['POST'])
def insert_teacher():
    data = request.get_json()
    if not Teacher.can_insert(data):
        abort(400, description='Missing teacher data.')
    username, fullname = data['username'].lower(), data['fullname'].lower()
    teacher = (Teacher
               .get_query()
               .filter(or_(
        db.func.lower(Teacher.username) == username,
        db.func.lower(Teacher.fullname) == fullname))
               .first())
    if teacher is not None:
        abort(400, description='The username/fullname is used.')
    teacher = Teacher.prepare_insert(data)
    if not teacher.insert():
        abort(400, description='Error while inserting teacher data.')
    return jsonify({
        'success': True,
        'teacher': Teacher.to_dict(teacher)
    })


@api.route('/teachers/<int:teacher_id>', methods=['PATCH'])
def update_teacher(teacher_id):
    teacher = Teacher.get_by_id(teacher_id)
    if teacher is None:
        abort(404, description='Teacher not found.')
    data = request.get_json()
    if not Teacher.can_update(data):
        abort(400, description='Nothing to update.')
    fullname = data['fullname'].lower()
    other_teacher = (Teacher
                     .get_query()
                     .filter(db.func.lower(Teacher.fullname) == fullname)
                     .first())
    if other_teacher is not None and other_teacher.id != teacher_id:
        abort(400, description='The fullname is already used.')
    teacher.prepare_update(data)
    if not teacher.update():
        abort(400, description='Error updating teacher.')
    return jsonify({
        'success': True,
        'teacher': Teacher.to_dict(teacher)
    })


@api.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    """
    Mark a teacher as archived. We don't delete information to preserve data
    integrity.
    """
    teacher = Teacher.get_by_id(teacher_id)
    if teacher is None:
        abort(404, description='Teacher not found.')
    teacher.is_archived = True
    teacher.dt_archive = datetime.now()
    if not teacher.update():
        abort(400, description='Error deleting teacher.')
    return jsonify({
        'success': True,
        'deleted': teacher_id
    })
