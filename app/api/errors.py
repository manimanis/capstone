from flask import jsonify
from werkzeug.exceptions import HTTPException
from . import api
from ..auth import AuthError


@api.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({
        'success': False,
        'code': e.code,
        'name': e.name,
        'description': e.description
    }), e.code


@api.errorhandler(AuthError)
def handle_exception(e):
    return jsonify({
        'success': False,
        'code': e.status_code,
        'name': e.error,
        'description': e.error
    }), e.code
