from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from server.cshr.models.users import User
from server.cshr.models.office import Office
from server.cshr.models.training_courses import Training_Courses

client = APIClient()


class TrainingCoursesTests(APITestCase):
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

    def test_create_training_courses(self) -> Training_Courses:
        url = "/api/training_courses/"
        data = {"name": "course12", "certificate_link": "string"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_training_courses_no_data(self) -> Training_Courses:
        url = "/api/training_courses/"
        data = {}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_creation_training_courses(self) -> Training_Courses:
        """test to get a valid training_courses"""
        """add training_courses"""
        url = "/api/training_courses/"
        data = {"name": "course12", "certificate_link": "string"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/training_courses/1/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_training_courses(self) -> Training_Courses:
        """test to get a valid training_courses"""
        """add training_courses"""
        url = "/api/training_courses/"
        data = {"name": "course12", "certificate_link": "string"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/training_courses/10/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_training_courses(self) -> Training_Courses:
        """test to delete a valid training_courses"""
        """add training_courses"""
        url = "/api/training_courses/"
        data = {"name": "course12", "certificate_link": "string"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/training_courses/1/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_training_courses(self) -> Training_Courses:
        """test to delete invalid compensation"""
        """add training_courses"""
        url = "/api/training_courses/"
        data = {"name": "course12", "certificate_link": "string"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/training_courses/10/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_training_courses(self) -> Training_Courses:
        """update training_courses"""
        url = "/api/training_courses/"
        data = {"name": "course12", "certificate_link": "string"}
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/training_courses/1/"
        data = {"user": 1}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
