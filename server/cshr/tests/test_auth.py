from rest_framework import status
from rest_framework.test import APITestCase
from server.cshr.models.users import User
from server.cshr.models.office import Office
from django.contrib.auth.hashers import make_password


class RegisterationTests(APITestCase):
    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")

        admin = User.objects.create(
            first_name="Jane",
            last_name="Brown",
            telegram_link="@janebrown",
            email="jane@gmail.com",
            birthday="1998-08-24",
            mobile_number="+201234567890",
            location=office,
            password=make_password("adminpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Admin",
            social_insurance_number="086 858 276",
            image="profile_image/default.png",
        )

        u1 = User.objects.create(
            first_name="John",
            last_name="Blake",
            telegram_link="@johnblake",
            email="john@outlook.com",
            birthday="2000-12-30",
            mobile_number="+201012345678",
            location=office,
            password=make_password("userpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="User",
            social_insurance_number="046 454 286",
            image="profile_image/default.png",
        )
        u1.reporting_to.set(
            [
                admin.id,
            ]
        )

        u2 = User.objects.create(
            first_name="Sarah",
            last_name="Poland",
            telegram_link="@sarahpoland",
            email="sarah@hotmail.com",
            birthday="1996-03-12",
            mobile_number="+201123456789",
            location=office,
            password=make_password("superpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Supervisor",
            social_insurance_number="121 212 121",
            image="profile_image/default.png",
        )
        u2.reporting_to.set(
            [
                admin.id,
            ]
        )

        self.access_token_admin = self.get_token_admin()
        self.access_token_user = self.get_token_user()
        self.access_token_supervisor = self.get_token_supervisor()

    def get_token_admin(self):
        """Get token for admin user."""
        url = "/api/auth/login/"
        data = {"email": "jane@gmail.com", "password": "adminpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["results"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = "/api/auth/login/"
        data = {"email": "john@outlook.com", "password": "userpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["results"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = "/api/auth/login/"
        data = {"email": "sarah@hotmail.com", "password": "superpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["results"]["access_token"]

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
            "reporting_to": [],
            "gender": "Male",
            "job_title": "developer",
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
            "email": "sarah@hotmail.com",
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
            first_name="Sarah",
            last_name="Poland",
            telegram_link="@sarahpoland",
            email="sarah@hotmail.com",
            birthday="1996-03-12",
            mobile_number="+201123456789",
            location=office,
            password=make_password("superpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Supervisor",
            social_insurance_number="121 212 121",
            image="profile_image/default.png",
        )

    def test_login_success(self):
        """
        Ensure we can login as a user.
        """
        url = "/api/auth/login/"
        data = {"email": "sarah@hotmail.com", "password": "superpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail_email(self):
        """
        a wrong email not able to login.
        """
        url = "/api/auth/login/"
        data = {"email": "user2@example.com", "password": "superpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_fail_pass(self):
        """
        a wrong pass not able to login.
        """
        url = "/api/auth/login/"
        data = {"email": "sarah@hotmail.com", "password": "password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
