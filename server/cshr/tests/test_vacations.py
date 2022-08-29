from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from server.cshr.models.users import User
from server.cshr.models.office import Office
from server.cshr.models.vacations import Vacation

client = APIClient()


class VacationsTests(APITestCase):
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

    def test_create_vacation(self) -> Vacation:
        url = "/api/vacations/"
        data = {
            "reason": "annual_leaves",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
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
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vacation_with_no_end_date(self) -> Vacation:
        url = "/api/vacations/"
        data = {"reason": "annual_leaves", "from_date": "2022-08-23", "change_log": 123}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vacation_with_no_from_date(self) -> Vacation:
        url = "/api/vacations/"
        data = {"reason": "annual_leaves", "end_date": "2022-08-23", "change_log": 123}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
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
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
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
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
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
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
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
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/vacations/10/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_vacation_requests(self) -> Vacation:
        """test to get all vacation requests"""
        url = "/api/vacations/"
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vacation_request(self) -> Vacation:
        """add vacation _request"""
        url = "/api/vacations/"
        data = {
            "reason": "annual_leaves",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_admin
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/vacations/edit/1/"
        data = {"applying_user": 1}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, 202)

    def test_update_vacation_request_not_authorized(self) -> Vacation:
        """add vacation _request"""
        url = "/api/vacations/"
        data = {
            "reason": "annual_leaves",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/vacations/edit/1/"
        data = {"applying_user": 1}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_update_vacation_request_invalid_user_id(self) -> Vacation:
        """add vacation request"""
        url = "/api/vacations/"
        data = {
            "reason": "annual_leaves",
            "from_date": "2022-08-23",
            "end_date": "2022-08-23",
            "change_log": 123,
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_admin
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/vacations/edit/1/"
        data = {"applying_user": -1}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
