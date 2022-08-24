from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from server.cshr.models.users import User
from server.cshr.models.office import Office
from server.cshr.models.compensation import Compensation

client = APIClient()


class CompensationTests(APITestCase):
    def setUp(self):
        """ make office and user object """
        office = Office.objects.create(name="testOffice", country="testCountry")
        self.office = office
        user = self.create_user()
        self.user = user
        self.access_token = self.get_token()
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token
        )

    def get_token(self):
        """Get token for logged in user."""
        url = f'{"/api/auth/login/"}'
        data = {"email": "user1@example.com", "password": "string"}

        response = client.post(url, data, format="json")
        print("123456677")
        print(response)
        print(response.data)
        return response.data["access_token"]

    def create_user(self) -> User:
        url = "/api/auth/signup/"
        data = {
            "first_name": "fname1",
            "last_name": "lname2",
            "telegram_link": "string",
            "email": "user1@example.com",
            "birthday": "2022-08-16",
            "mobile_number": "01234567890",
            "password": "string",
            "team": "Development",
            "user_type": "User",
            "location": 1,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_compensation(self) -> Compensation:
        url = "/api/compensation/"
        data = {"reason": "string", "from_date": "2022-08-24", "end_date": "2022-08-24"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_compensation_no_data(self) -> Compensation:
        url = "/api/compensation/"
        data = {}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_creation_compensation(self) -> Compensation:
        """test to get a valid compensation"""
        """add compensation"""
        url = "/api/compensation/"
        data = {"reason": "string", "from_date": "2022-08-24", "end_date": "2022-08-24"}
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
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
