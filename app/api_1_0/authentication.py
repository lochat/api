from flask import g, jsonify, request, url_for, current_app
from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ..models import User
from ..email import send_email
from .errors import unauthorized, bad_request, forbidden
from . import api
auth = HTTPBasicAuth()


def generate_token(user, expiration):
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    return s.dumps({'id': str(user.id)})


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return None
    return User.objects.get(id=data['id'])


@auth.verify_password
def verify_password(email_or_token, password):
    if password == '':
        g.current_user = verify_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.objects.filter(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@api.before_request
def only_register():
    if request.endpoint == 'api.register' and request.method == 'POST':
        return register()


@api.before_request
@auth.login_required
def before_request():
    if request.endpoint == 'api.confirm':
        token = request.view_args['token']
        return confirm(token)
    if not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.route('/get_token')
@auth.login_required
def get_token():
    if g.token_used:
        return unauthorized('Invalid credentials')
    token = generate_token(g.current_user, 3600).decode('utf-8')
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

    if User.objects.filter(username=attrs[0]).first() is not None:
        return bad_request("Email already registered.")

    if User.objects.filter(email=attrs[1]).first() is not None:
        return bad_request("Username already in use.")

    user = User(username=attrs[0], email=attrs[1])
    user.password = attrs[2]
    user.save()
    token = generate_token(user, 3600)
    send_email(user.email, 'Confirm Your Account',
               'auth/mail/confirm', username=user.username, token=token)
    location = {'Location': url_for('api.get_user',
                                    username=user.username,
                                    _external=True)}
    message = 'Confirm your account, \
        if you received an email with a confirmation link.'
    return jsonify({'message': message}), 201, location


@api.route('/confirm/<token>')
@auth.login_required
def confirm(token):
    if g.current_user.confirmed:
        return jsonify({'Location': url_for('api.get_user',
                                            username=g.current_user.username,
                                            _external=True)})
    user = verify_token(token)
    if user and user.id == g.current_user.id:
        user.confirmed = True
        user.save()
        return jsonify({'message': 'You have confirmed your account. Thanks!'})
    else:
        return jsonify(
            {'message': 'The confirmation link is invalid or has expired!'}
        )


@api.route('/confirm')
@auth.login_required
def resend_confirmation():
    token = generate_token(g.current_user, 3600)
    send_email(g.current_user.email, 'Confirm Your Account',
               'auth/mail/confirm', username=g.current_user.username,
               token=token)

    return jsonify(
        {'message': 'Confirm your account, \
         if you received an email with a confirmation link.'}
    )
