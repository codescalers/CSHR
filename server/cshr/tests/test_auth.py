from rest_framework import status
from rest_framework.test import APITestCase
from server.cshr.models.users import User
from server.cshr.models.office import Office


class RegisterationTests(APITestCase):
    def setUp(self):
        Office.objects.create(name="testOffice", country="testCountry")

    def test_register_user(self) -> User:
        """
        Ensure we can create a user account.
        """
        url = "/api/auth/signup/"
        data = {
            "first_name": "fname1",
            "last_name": "lname2",
            "telegram_link": "string",
            "email": "user1@example.com",
            "birthday": "2022-08-16",
            "mobile_number": "01234567890",
            "password": "password",
            "location": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_non_existing_location(self) -> User:
        """
        creating a user with a non existing location is not allowed
        """
        url = "/api/auth/signup/"
        data = {
            "first_name": "alia2",
            "last_name": "saddik2",
            "telegram_link": "string",
            "email": "user252@example.com",
            "birthday": "2022-08-25",
            "mobile_number": "01928389476",
            "password": "password2",
            "location": 2,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_same_mail(self) -> User:
        """
        creating a user with an existing mail is not allowed
        """
        self.test_register_user()
        url = "/api/auth/signup/"
        data = {
            "first_name": "alia2",
            "last_name": "saddik2",
            "telegram_link": "string",
            "email": "user1@example.com",
            "birthday": "2022-08-25",
            "mobile_number": "01928389476",
            "password": "password2",
            "location": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def setUp(self):
        Office.objects.create(name="testOffice", country="testCountry")
        self.create_user()

    def create_user(self) -> User:
        url = "/api/auth/signup/"
        data = {
            "first_name": "fname1",
            "last_name": "lname2",
            "telegram_link": "string",
            "email": "user1@example.com",
            "birthday": "2022-08-16",
            "mobile_number": "01234567890",
            "password": "password",
            "location": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_success(self):
        """
        Ensure we can login as auser.
        """
        url = "/api/auth/login/"
        data = {"email": "user1@example.com", "password": "password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail_email(self):
        """
        a wrong email not able to login.
        """
        url = "/api/auth/login/"
        data = {"email": "user2@example.com", "password": "password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_fail_pass(self):
        """
        a wrong pass not able to login.
        """
        url = "/api/auth/login/"
        data = {"email": "user1@example.com", "password": "password2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
