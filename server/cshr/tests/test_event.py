from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from server.cshr.models.users import User
from server.cshr.models.office import Office
from server.cshr.models.event import Event
from django.contrib.auth.hashers import make_password

client = APIClient()


class EventTests(APITestCase):
    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")

        User.objects.create(
            first_name="Ahmed",
            last_name="Mohamed",
            telegram_link="https://t.me/ahmed2",
            email="ahmed@gmail.com",
            birthday="1995-08-24",
            mobile_number="0123456789",
            password=make_password("ahmedpass"),
            location=office,
            team="Development",
            user_type="Admin",
        )

        User.objects.create(
            first_name="Andrew",
            last_name="Nassef",
            telegram_link="https://t.me/andrew",
            email="andrew@gmail.com",
            birthday="2001-08-24",
            mobile_number="010234567",
            password=make_password("andrewpass"),
            location=office,
            team="Development",
            user_type="User",
        )

        User.objects.create(
            first_name="Helmy",
            last_name="Bakr",
            telegram_link="https://t.me/helmy",
            email="helmy@gmail.com",
            birthday="2000-08-24",
            mobile_number="01238512",
            password=make_password("helmypass"),
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
        data = {"email": "ahmed@gmail.com", "password": "ahmedpass"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = f'{"/api/auth/login/"}'
        data = {"email": "andrew@gmail.com", "password": "andrewpass"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = f'{"/api/auth/login/"}'
        data = {"email": "helmy@gmail.com", "password": "helmypass"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def test_create_event(self) -> Event:
        url = "/api/event/"
        data = {
            "name": "test event",
            "description": "our first test event",
            "people": [1, 2],
            "location": "Cairo Egypt",
            "from_date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "end_date": {"year": 2022, "month": 9, "day": 9, "hour": 16, "minute": 24},
        }
        # editted here
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_no_event_location(self) -> Event:
        url = "/api/event/"
        data = {
            "name": "test event",
            "description": "our first test event",
            "people": [1, 2],
            "from_date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "end_date": {"year": 2022, "month": 9, "day": 9, "hour": 16, "minute": 24},
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_no_people(self) -> Event:
        url = "/api/event/"
        data = {
            "name": "test event",
            "description": "our first test event",
            "people": [],
            "location": "Cairo Egypt",
            "from_date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "end_date": {"year": 2022, "month": 9, "day": 9, "hour": 16, "minute": 24},
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_certain_event(self) -> Event:
        """test to get a valid event"""
        """add event"""
        url = "/api/event/"
        data = {
            "name": "test event",
            "description": "our first test event",
            "people": [1, 2],
            "location": "Cairo Egypt",
            "from_date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "end_date": {"year": 2022, "month": 9, "day": 9, "hour": 16, "minute": 24},
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/event/1/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_event(self) -> Event:
        """test to get  invalid event"""
        """add event"""
        url = "/api/event/"
        data = {
            "name": "test event",
            "description": "our first test event",
            "people": [1, 2],
            "location": "Cairo Egypt",
            "from_date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "end_date": {"year": 2022, "month": 9, "day": 9, "hour": 16, "minute": 24},
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/event/10/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_certain_event(self) -> Event:
        """test to delete a valid event"""
        """add event"""
        url = "/api/event/"
        data = {
            "name": "test event",
            "description": "our first test event",
            "people": [1, 2],
            "location": "Cairo Egypt",
            "from_date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "end_date": {"year": 2022, "month": 9, "day": 9, "hour": 16, "minute": 24},
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/event/1/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_event(self) -> Event:
        """test to delete invalid event"""
        url = "/api/event/10/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_events(self) -> Event:
        """test to get all events"""
        url = "/api/event/"
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_event(self) -> Event:
        """update event"""
        url = "/api/event/"
        data = {
            "name": "test event",
            "description": "our first test event",
            "people": [1, 2],
            "location": "Cairo Egypt",
            "from_date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "end_date": {"year": 2022, "month": 9, "day": 9, "hour": 16, "minute": 24},
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/event/1/"
        data = {"description": "updated event description"}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, 202)

    def test_update_event_invalid_people(self) -> Event:
        """update event"""
        url = "/api/event/"
        data = {
            "name": "test event",
            "description": "our first test event",
            "location": "Cairo Egypt",
            "people": [1],
            "from_date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "end_date": {"year": 2022, "month": 9, "day": 9, "hour": 16, "minute": 24},
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/event/1/"
        data["people"] = [-50]
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_event_invalid_date_format(self) -> Event:
        """create event with no date"""
        url = "/api/event/"
        data = {
            "name": "Shelby Austin",
            "description": "Eius odio recusandae Ipsa consectetur vitae culpa aliquid veniam reiciendis numquam \
                sed quae aut iusto rerum vel nihil neque et",
            "location": "Deserunt amet aut saepe autem id eveniet non aliquip voluptas minima cupiditate nostrud hic ea",
            "date": "2022-08-23ds",
            "people": [1],
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
