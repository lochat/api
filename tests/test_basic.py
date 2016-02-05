import unittest
import json
from flask import current_app, url_for
from app import create_app, db
from mongoengine.context_managers import switch_db
from app.models import User


class BasicsTestCase(unittest.TestCase):
    def setUp(self):

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.register_connection('test', self.app.config['MONGODB_DB'])
        self.client = self.app.test_client()

    def tearDown(self):
        namedb = self.app.config['MONGODB_DB']
        client = db.connect(namedb)
        client.drop_database(namedb)
        self.app_context.pop()

    def test_example(self):
        response = self.client.get(url_for('api.test'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['result'] == 'Hello, World')

    def test_db(self):
        with switch_db(User, 'test') as UserTest:
            user = UserTest(name='teste', password='teste12')
            user.switch_db('test').save()
            user_persist = UserTest.objects.get(name='teste')
            self.assertTrue(user_persist.password == user.password)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
