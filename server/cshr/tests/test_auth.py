from rest_framework import status
from rest_framework.test import APITestCase
from server.cshr.models.users import User


class AuthenticationTests(APITestCase):
    def test_register_user(self) -> User:
        """
        Ensure we can create a user account.
        """
        url = "/api/auth/signup/"
        data = {
            "first_name": "alianew",
            "last_name": "saddikaaa",
            "telegram_link": "string",
            "email": "user25201@example.com",
            "birthday": "2022-08-16",
            "mobile_number": "9389384298230",
            "password": "password",
            "location": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
