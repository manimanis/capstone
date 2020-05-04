from flask import jsonify, request
from . import api

# To be deleted


@api.route('/test')
def test():
    return jsonify({'myname': 'Mohamed Anis MANI'})
