from flask import jsonify
from . import api


@api.route('/')
def test():
    return jsonify({'result': 'Hello, World'}), 200
