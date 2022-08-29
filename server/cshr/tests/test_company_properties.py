from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from server.cshr.models.users import User
from server.cshr.models.office import Office
from server.cshr.models.company_properties import Company_properties


client = APIClient()


class CompanyPropertiesTests(APITestCase):
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

    def test_create_company_properties(self) -> Company_properties:
        url = "/api/company_properties/"
        data = {
            "name": "string",
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_company_properties_no_data(self) -> Company_properties:
        url = "/api/company_properties/"
        data = {}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_creation_company_properties(self) -> Company_properties:
        """test to get a valid company_properties"""
        """add company_properties"""
        url = "/api/company_properties/"
        data = {
            "name": "string",
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/company_properties/1/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_company_properties(self) -> Company_properties:
        """test to get a valid company_properties"""
        """add company_properties"""
        url = "/api/company_properties/"
        data = {
            "name": "string",
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/company_properties/10/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_company_properties(self) -> Company_properties:
        """test to delete a valid company_properties"""
        """add company_properties"""
        url = "/api/company_properties/"
        data = {
            "name": "string",
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/company_properties/1/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_company_properties(self) -> Company_properties:
        """test to delete invalid compensation"""
        """add company_properties"""
        url = "/api/company_properties/"
        data = {
            "name": "string",
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/company_properties/10/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_company_properties(self) -> Company_properties:
        """update company_properties"""
        url = "/api/company_properties/"
        data = {
            "name": "string",
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/company_properties/1/"
        data = {"user": 1}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
