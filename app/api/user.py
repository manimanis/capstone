from datetime import datetime

from flask import jsonify, request, abort
from sqlalchemy import or_

from . import api, read_request_args
from .. import db
from ..auth import requires_auth
from ..models import User


@api.route('/users')
@requires_auth('users:get')
def get_users(payload):
    """Returns a list of users"""
    start, end, search = read_request_args()
    query = User.text_search(search)
    search_count = query.count()
    users_count = User.get_query().count()
    start, end = max(start, 0), min(end, search_count)
    users = User.to_list_of_dict(query.slice(start, end))
    return jsonify({
        'success': True,
        'users_count': users_count,
        'search_count': search_count,
        'start': start,
        'end': end,
        'users': users
    })


@api.route('/users/<int:user_id>')
@requires_auth('users:get')
def get_user_by_id(payload, user_id):
    """Returns a single user by its id"""
    user = User.get_by_id(user_id)
    if user is None:
        abort(404, description='User not found')
    return jsonify({
        'success': True,
        'user': User.to_dict(user)
    })


@api.route('/users', methods=['POST'])
@requires_auth('users:post')
def insert_user(payload):
    data = request.get_json()
    if not User.can_insert(data):
        abort(400, description='Missing user data.')
    username, fullname = data['username'].lower(), data['fullname'].lower()
    user = (User
            .get_query()
            .filter(or_(db.func.lower(User.username) == username,
                        db.func.lower(User.fullname) == fullname))
            .first())
    if user is not None:
        abort(400, description='The username/fullname is used.')
    user = User.prepare_insert(data)
    if not user.insert():
        abort(400, description='Error while inserting user data.')
    return jsonify({
        'success': True,
        'user': User.to_dict(user)
    })


@api.route('/users/<int:user_id>', methods=['PATCH'])
@requires_auth('users:patch')
def update_user(payload, user_id):
    user = User.get_by_id(user_id)
    if user is None:
        abort(404, description='User not found.')
    data = request.get_json()
    if not User.can_update(data):
        abort(400, description='Nothing to update.')
    fullname = data['fullname'].lower()
    other_user = (User
                  .get_query()
                  .filter(db.func.lower(User.fullname) == fullname)
                  .first())
    if other_user is not None and other_user.id != user_id:
        abort(400, description='The fullname is already used.')
    user.prepare_update(data)
    if not user.update():
        abort(400, description='Error updating user.')
    return jsonify({
        'success': True,
        'user': User.to_dict(user)
    })


@api.route('/users/<int:user_id>', methods=['DELETE'])
@requires_auth('users:post')
def delete_user(payload, user_id):
    """
    Mark a user as archived. We don't delete information to preserve data
    integrity.
    """
    user = User.get_by_id(user_id)
    if user is None:
        abort(404, description='User not found.')
    user.is_archived = True
    user.dt_archive = datetime.now()
    if not user.update():
        abort(400, description='Error deleting user.')
    return jsonify({
        'success': True,
        'deleted': user_id
    })
