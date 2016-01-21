from flask import jsonify


def index():
    return jsonify({'result': 'Hello World'})
