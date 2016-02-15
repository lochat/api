from flask import g, jsonify, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
from ..models import User
from .errors import unauthorized, bad_request
from . import api
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.objects.filter(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.route('/token')
@auth.login_required
def get_token():
    if g.token_used:
        return unauthorized('Invalid credentials')
    token = g.current_user.generate_auth_token(expiration=3600).decode('utf-8')
    return jsonify(
        {'token': token,
         'expiration': 3600})


@api.route('/register', methods=['POST'])
def register():
    attrs = (
        request.json.get('username'),
        request.json.get('email'),
        request.json.get('password')
    )

    if not all(attrs):
        return bad_request("The request cannot be fulfilled due to bad syntax.")

    if User.objects.filter(email=attrs[1]).first() is not None:
        return bad_request("The request cannot be fulfilled due to bad syntax.")

    user = User(username=attrs[0], email=attrs[1])
    user.password = attrs[2]
    user.save()

    location = {'Location': url_for('api.get_user',
                                    username=user.username,
                                    _external=True)}
    return jsonify({'username': user.username}), 201, location
