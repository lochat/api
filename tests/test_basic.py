import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
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

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
