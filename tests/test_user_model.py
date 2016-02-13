import unittest
from app.models import User


class TestUserModel(unittest.TestCase):

    """Password hashing tests"""

    def test_password_setter(self):
        u = User()
        u.password = 'cat'
        self.assertTrue(u.password_hash is not True)

    def test_no_password_getter(self):
        u = User()
        u.password = 'cat'
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User()
        u.password = 'cat'
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User()
        u.password = 'cat'
        u2 = User()
        u2.password = 'cat'
        self.assertTrue(u.password_hash != u2.password_hash)
