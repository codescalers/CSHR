from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from server.cshr.models.users import User
from server.cshr.models.office import Office
from server.cshr.models.vacations import Vacation

client = APIClient()


class VacationsTests(APITestCase):
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

    def test_create_vacation(self) -> Vacation:
        url = "/api/vacations/"
        data = {
            "reason": "annual_leaves",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vacation_with_invalid_reason(self) -> Vacation:
        url = "/api/vacations/"
        data = {
            "reason": "invalid",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vacation_with_no_end_date(self) -> Vacation:
        url = "/api/vacations/"
        data = {"reason": "annual_leaves", "from_date": "2022-08-23", "change_log": 123}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vacation_with_no_from_date(self) -> Vacation:
        url = "/api/vacations/"
        data = {"reason": "annual_leaves", "end_date": "2022-08-23", "change_log": 123}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_certain_vacation_request(self) -> Vacation:
        """test to get a valid vacation request"""
        """add vacation"""
        url = "/api/vacations/"
        data = {
            "reason": "annual_leaves",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/vacations/1/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_vacation_request(self) -> Vacation:
        """test to get a invalid vacation request"""
        """add vacation"""
        url = "/api/vacations/"
        data = {
            "reason": "annual_leaves",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/vacations/10/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_certain_vacation_request(self) -> Vacation:
        """test to delete a valid vacation request"""
        """add vacation request"""
        url = "/api/vacations/"
        data = {
            "reason": "annual_leaves",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/vacations/1/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_vacation_request(self) -> Vacation:
        """test to delete a invalid vacation request"""
        """add vacation request"""
        url = "/api/vacations/"
        data = {
            "reason": "annual_leaves",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/vacations/10/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_update_vacation_request(self) -> Vacation:
            """add vacation _request"""
            url = "/api/vacations/"
            data = {
                "reason": "annual_leaves",
                "from_date": "2022-08-23",
                "end_date": "2022-08-23",
                "change_log": 123,
            }
            response = client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            url = "/api/vacations/edit/1/"
            data = {"applying_user": 1}
            response = client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vacation_request_invalid_user_id(self) -> Vacation:
        """add vacation request"""
        url = "/api/vacations/"
        data = {
            "reason": "annual_leaves",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/vacations/edit/1/"
        data = {"applying_user": -1}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_vacation_requests(self) -> Vacation:
        """test to get all vacation requests"""
        url = "/api/vacations/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
