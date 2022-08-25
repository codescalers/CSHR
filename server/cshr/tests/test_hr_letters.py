from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from server.cshr.models.users import User
from server.cshr.models.office import Office
from server.cshr.models.hr_letters import HR_LETTERS

client = APIClient()


class HrLetterTests(APITestCase):
    def setUp(self):
        """make office and user object"""
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
        data = {"email": "user1@example.com", "password": "password"}
        response = client.post(url, data, format="json")
        return response.data["data"]["access_token"]

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

    def test_create_hr_letter(self) -> HR_LETTERS:
        url = "/api/hrletter/"
        data = {"addresses": "testing addr"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_hr_letter_no_address(self) -> HR_LETTERS:
        url = "/api/hrletter/"
        data = {}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_certain_hr_letters(self) -> HR_LETTERS:
        """test to get a valid hr letter"""
        """add hr letter"""
        url = "/api/hrletter/"
        data = {"addresses": "testing addr"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hrletter/1/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_hr_letter(self) -> HR_LETTERS:
        """test to get a valid hr letter"""
        """add hr letter"""
        url = "/api/hrletter/"
        data = {"addresses": "testing addr"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hrletter/10/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_certain_hr_letters(self) -> HR_LETTERS:
        """test to delete a valid hr letter"""
        """add hr letter"""
        url = "/api/hrletter/"
        data = {"addresses": "testing addr"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hrletter/1/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_hr_letters(self) -> HR_LETTERS:
        """test to delete invalid hr letter"""
        """add hr letter"""
        url = "/api/hrletter/"
        data = {"addresses": "testing addr"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hrletter/10/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_hr_letters(self) -> HR_LETTERS:
        """test to get all hr letters"""
        url = "/api/hrletter/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HrLetterUpdateTests(APITestCase):
    def setUp(self):
        """make office and user object"""
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
        data = {"email": "user1@example.com", "password": "password"}
        response = client.post(url, data, format="json")
        return response.data["data"]["access_token"]

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
            "user_type": "admin",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_hr_letter(self) -> HR_LETTERS:
        """update hr letter"""
        url = "/api/hrletter/"
        data = {"addresses": "testing addr"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hrletter/edit/1/"
        data = {"applying_user": 1}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_hr_letter_invalid_user_id(self) -> HR_LETTERS:
        """update hr letter"""
        url = "/api/hrletter/"
        data = {"addresses": "testing addr"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hrletter/edit/1/"
        data = {"applying_user": -1}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
