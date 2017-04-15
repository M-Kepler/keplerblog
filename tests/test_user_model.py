import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(passwd='')
        self.assertTrue(u.passwd_hash is not None)

    def test_no_password_getter(self):
        u = User(passwd='')
        with self.assertRaises(AttributeError):
            u.passwd

    def test_password_verfication(self):
        u = User(passwd='')
        self.assertTrue(u.verify_password(''))
        self.assertFalse(u.verify_password(''))

    def test_password_salts_are_random(self):
        u = User(passwd='')
        u2=User(passwd='')
        self.assertTrue(u.passwd_hash != u2.passwd_hash)

