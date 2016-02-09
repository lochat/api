from flask import jsonify
from . import api


@api.app_errorhandler(404)
def not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
