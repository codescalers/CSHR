from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from server.cshr.models.users import User
from server.cshr.models.office import Office
from server.cshr.models.compensation import Compensation

client = APIClient()


class CompensationTests(APITestCase):
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
        url = f'{"/api/auth/login/"}'
        data = {"email": "user1@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = f'{"/api/auth/login/"}'
        data = {"email": "user2@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = f'{"/api/auth/login/"}'
        data = {"email": "user3@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def test_create_compensation(self) -> Compensation:
        url = "/api/compensation/"
        data = {"reason": "string", "from_date": "2022-08-24", "end_date": "2022-08-24"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_compensation_no_data(self) -> Compensation:
        url = "/api/compensation/"
        data = {}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_creation_compensation(self) -> Compensation:
        """test to get a valid compensation"""
        """add compensation"""
        url = "/api/compensation/"
        data = {"reason": "string", "from_date": "2022-08-24", "end_date": "2022-08-24"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/compensation/1/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_compensation(self) -> Compensation:
        """test to get a valid compensation"""
        """add compensation"""
        url = "/api/compensation/"
        data = {"reason": "string", "from_date": "2022-08-24", "end_date": "2022-08-24"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/compensation/10/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_compensation(self) -> Compensation:
        """test to delete a valid compensation"""
        """add compensation"""
        url = "/api/compensation/"
        data = {"reason": "string", "from_date": "2022-08-24", "end_date": "2022-08-24"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/compensation/1/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_compensation(self) -> Compensation:
        """test to delete invalid compensation"""
        """add compensation"""
        url = "/api/compensation/"
        data = {"reason": "string", "from_date": "2022-08-24", "end_date": "2022-08-24"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/compensation/10/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_compensation(self) -> Compensation:
        """update compensation"""
        url = "/api/compensation/"
        data = {"reason": "string", "from_date": "2022-08-24", "end_date": "2022-08-24"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/compensation/1/"
        data = {"user": 1}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
