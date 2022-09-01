from rest_framework import status
from rest_framework.test import APITestCase
from server.cshr.models.users import User
from server.cshr.models.office import Office


class RegisterationTests(APITestCase):
    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")

        User.objects.create(
            first_name="string",
            last_name="string",
            telegram_link="string",
            email="user1@example.com",
            birthday="2022-08-24",
            mobile_number="string",
            password="pbkdf2_sha256$390000$VjStUZfdq3LyQ7PvGwnJNj$Niy9PAOmqWe2dqkML40hWWBgibzQDHz5ZZVKSdhIOIQ=",
            location=office,
            team="Development",
            user_type="Admin",
        )

        User.objects.create(
            first_name="string",
            last_name="string",
            telegram_link="string",
            email="user2@example.com",
            birthday="2022-08-24",
            mobile_number="string",
            password="pbkdf2_sha256$390000$VjStUZfdq3LyQ7PvGwnJNj$Niy9PAOmqWe2dqkML40hWWBgibzQDHz5ZZVKSdhIOIQ=",
            location=office,
            team="Development",
            user_type="User",
        )

        User.objects.create(
            first_name="string",
            last_name="string",
            telegram_link="string",
            email="user3@example.com",
            birthday="2022-08-24",
            mobile_number="string",
            password="pbkdf2_sha256$390000$VjStUZfdq3LyQ7PvGwnJNj$Niy9PAOmqWe2dqkML40hWWBgibzQDHz5ZZVKSdhIOIQ=",
            location=office,
            team="Development",
            user_type="Supervisor",
        )

        self.access_token_admin = self.get_token_admin()
        self.access_token_user = self.get_token_user()
        self.access_token_supervisor = self.get_token_supervisor()

    def get_token_admin(self):
        """Get token for admin user."""
        url = "/api/auth/login/"
        data = {"email": "user1@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = "/api/auth/login/"
        data = {"email": "user2@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = "/api/auth/login/"
        data = {"email": "user3@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def test_register_user_admin(self) -> User:
        """
        Ensure we can create a user account as an admin.
        """
        url = "/api/auth/signup/"
        data = {
            "first_name": "string",
            "last_name": "string",
            "telegram_link": "string",
            "email": "user@example.com",
            "birthday": "2022-08-24",
            "mobile_number": "string",
            "password": "string",
            "location": 1,
            "team": "Development",
            "salary": {"gross": 1000},
            "user_type": "User",
            "reporting_to": 1,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_non_existing_location_admin(self) -> User:
        """
        creating a user with a non existing location is not allowed
        """
        url = "/api/auth/signup/"
        data = {
            "first_name": "string",
            "last_name": "string",
            "telegram_link": "string",
            "email": "user@example.com",
            "birthday": "2022-08-24",
            "mobile_number": "string",
            "password": "string",
            "location": 2,
            "team": "Development",
            "salary": {"gross": 1000},
            "user_type": "User",
            "reporting_to": 1,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_same_mail_admin(self) -> User:
        """
        creating a user with an existing mail is not allowed
        """

        url = "/api/auth/signup/"
        data = {
            "first_name": "string",
            "last_name": "string",
            "telegram_link": "string",
            "email": "user1@example.com",
            "birthday": "2022-08-24",
            "mobile_number": "string",
            "password": "string",
            "location": 1,
            "team": "Development",
            "salary": {"gross": 1000},
            "user_type": "User",
            "reporting_to": 1,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_by_normal_user(self) -> User:
        """
        a normal user cannot register another user
        """
        url = "/api/auth/signup/"
        data = {
            "first_name": "string",
            "last_name": "string",
            "telegram_link": "string",
            "email": "user@example.com",
            "birthday": "2022-08-24",
            "mobile_number": "string",
            "password": "string",
            "location": 1,
            "team": "Development",
            "salary": {"gross": 1000},
            "user_type": "User",
            "reporting_to": 1,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_user_by_supervisor(self) -> User:
        """
        a supervisor user cannot register another user
        """
        url = "/api/auth/signup/"
        data = {
            "first_name": "string",
            "last_name": "string",
            "telegram_link": "string",
            "email": "user@example.com",
            "birthday": "2022-08-24",
            "mobile_number": "string",
            "password": "string",
            "location": 1,
            "team": "Development",
            "salary": {"gross": 1000},
            "user_type": "User",
            "reporting_to": 1,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoginTests(APITestCase):
    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")
        User.objects.create(
            first_name="string",
            last_name="string",
            telegram_link="string",
            email="user@example.com",
            birthday="2022-08-24",
            mobile_number="string",
            password="pbkdf2_sha256$390000$VjStUZfdq3LyQ7PvGwnJNj$Niy9PAOmqWe2dqkML40hWWBgibzQDHz5ZZVKSdhIOIQ=",
            location=office,
            team="Development",
            user_type="User",
        )

    def test_login_success(self):
        """
        Ensure we can login as a user.
        """
        url = "/api/auth/login/"
        data = {"email": "user@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail_email(self):
        """
        a wrong email not able to login.
        """
        url = "/api/auth/login/"
        data = {"email": "user2@example.com", "password": "password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_fail_pass(self):
        """
        a wrong pass not able to login.
        """
        url = "/api/auth/login/"
        data = {"email": "user1@example.com", "password": "password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
