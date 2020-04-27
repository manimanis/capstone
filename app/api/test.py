from flask import jsonify, request
from . import api


@api.route('/test')
def test():
    return jsonify({'myname': 'Mohamed Anis MANI'})