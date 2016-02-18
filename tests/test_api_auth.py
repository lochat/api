import unittest
import json
from flask import url_for
from app import create_app, db
from app.api_1_0 import authentication as auth
from base64 import b64encode
from app.models import User


class TestAPIAuth(unittest.TestCase):

    """API auth testing with Flask test client"""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        namedb = self.app.config['MONGODB_DB']
        client = db.connect(namedb)
        client.drop_database(namedb)
        self.app_context.pop()

    def get_api_headers(self, username, password):
        """TODO: Docstring for get_api_headers.

        :username: TODO
        :password: TODO
        :returns: TODO

        """
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application;json'
        }

    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers=self.get_api_headers('email', 'password'))
        self.assertTrue(response.status_code == 404)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'not found')

    def test_invalid_credentials(self):
        # add a user
        u = User(username='jim', email='jim@gmail.com', confirmed=True)
        u.password = 'cat'
        u.save()

        # authenticate with bad password
        response = self.client.get(
            url_for('api.resend_confirmation'),
            headers=self.get_api_headers('jim@gmail.com', 'dog'))

        self.assertTrue(response.status_code == 401)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'unauthorized')

    def test_token_auth(self):
        # add a user
        u = User(username='pam', email='pam@gmail.com', confirmed=True)
        u.password = 'dog'
        u.save()

        # issue a request with bad token
        response = self.client.get(
            url_for('api.get_user', username='pam'),
            headers=self.get_api_headers('badtoken', ''))
        self.assertTrue(response.status_code == 401)

        # get a token
        response = self.client.get(
            url_for('api.get_token'),
            headers=self.get_api_headers('pam@gmail.com', 'dog'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        # issue a request with the token
        response = self.client.get(
            url_for('api.get_user', username='pam'),
            headers=self.get_api_headers(token, ''))
        self.assertTrue(response.status_code == 200)

    def test_unconfirmed_account(self):
        # add a unconfirmed user
        u = User(username='pam', email='pam@gmail.com', confirmed=False)
        u.password = 'dog'
        u.save()

        # get user with unconfirmed account
        response = self.client.get(
            url_for('api.get_user', username='pam'),
            headers=self.get_api_headers('pam@gmail.com', 'dog'))
        self.assertTrue(response.status_code == 403)

    def test_get_user(self):
        # Add a user
        u = User(username='pam', email='pam@gmail.com', confirmed=True)
        u.password = 'dog'
        u.save()

        # get user with confirmed account
        response = self.client.get(
            url_for('api.get_user', username='pam'),
            headers=self.get_api_headers('pam@gmail.com', 'dog'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['email'] == 'pam@gmail.com')

    def test_register(self):
        # register a account
        response = self.client.post(
            url_for('api.register'),
            content_type='application/json',
            data=json.dumps({'username': 'michael',
                             'email': 'michael@gmail.com',
                             'password': 'mike12'})
        )

        self.assertEqual(response.status_code, 201)

        # get user with new account
        response = self.client.get(
            url_for('api.get_user', username='michael'),
            headers=self.get_api_headers('michael@gmail.com', 'mike12'))
        self.assertEqual(response.status_code, 403)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'forbidden')

        # send a confirmation token
        user = User.objects.filter(username='michael').first()
        token = auth.generate_token(user, 3600).decode('utf-8')
        user.confirmed = True
        user.save()
        response = self.client.get(
            url_for('api.get_user', username='michael'),
            headers=self.get_api_headers(token, ''))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['username'] == 'michael')
