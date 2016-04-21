import json
from flask import jsonify
from .authentication import auth
from ..models import User
from . import api


@api.route('/users/<username>')
@auth.login_required
def get_user(username):
    dict_json = json.loads(User.objects.get(username=username).to_json())
    dict_json.pop('password_hash')
    return jsonify(dict_json)
