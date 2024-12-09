# automated tests for the authentication

import unittest
from app import create_app, db
import json


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            'email': 'admin@gmail.com',
            'password': 'password'
        }
        with self.app.app_context():
            db.create_all()

    def test_registered_user_login(self):
        # Attempt to log in with the registered user
        res = self.client().post('/api/auth/login', json=self.user_data)

        # Parse the JSON response
        result = res.get_json()

        # Assertions
        self.assertIsNotNone(result.get('access_token'))
        self.assertEqual(res.status_code, 200)

    def test_non_registered_user_login(self):
        user_data = {
            'email': 'admin123@mail.com',
            'password': 'password'
        }
        res = self.client().post('/api/auth/login', json=user_data)
        result = res.get_json()

        self.assertEqual(result['msg'], 'Invalid email or password')

        self.assertEqual(res.status_code, 401)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()


# Run the tests
# python -m unittest discover -s tests -p "test_*.py"
