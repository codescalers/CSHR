from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from server.cshr.models.users import User
from server.cshr.models.office import Office
from server.cshr.models.meetings import Meetings
from django.contrib.auth.hashers import make_password

client = APIClient()


class MeetingsTests(APITestCase):
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
            user_type="TeamLead",
        )

        self.access_token_admin = self.get_token_admin()
        self.access_token_user = self.get_token_user()
        self.access_token_team_lead = self.get_token_team_lead()

    def get_token_admin(self):
        """Get token for admin user."""
        url = f'{"/api/auth/login/"}'
        data = {"email": "ahmed@gmail.com", "password": "ahmedpass"}
        response = self.client.post(url, data, format="json")
        return response.data["results"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = f'{"/api/auth/login/"}'
        data = {"email": "andrew@gmail.com", "password": "andrewpass"}
        response = self.client.post(url, data, format="json")
        return response.data["results"]["access_token"]

    def get_token_team_lead(self):
        """Get token for a team_lead user."""
        url = f'{"/api/auth/login/"}'
        data = {"email": "helmy@gmail.com", "password": "helmypass"}
        response = self.client.post(url, data, format="json")
        return response.data["results"]["access_token"]

    def test_create_meeting(self) -> Meetings:
        url = "/api/meeting/"
        data = {
            "meeting_link": "meeting link",
            "date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "invited_users": [1, 2],
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_meeting_no_meeting_link(self) -> Meetings:
        url = "/api/meeting/"
        data = {
            "date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "invited_users": [1, 2],
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_certain_meeting(self) -> Meetings:
        """test to get a valid meeting"""
        """add meeting"""
        url = "/api/meeting/"
        data = {
            "meeting_link": "meeting link",
            "date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "invited_users": [1, 2],
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/meeting/1/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_meeting(self) -> Meetings:
        """test to get a valid meeting"""
        """add meeting"""
        url = "/api/meeting/"
        data = {
            "meeting_link": "meeting link",
            "date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "invited_users": [1, 2],
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/meeting/10/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_certain_meeting(self) -> Meetings:
        """test to delete a valid meeting"""
        """add meeting"""
        url = "/api/meeting/"
        data = {
            "meeting_link": "meeting link",
            "date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "invited_users": [1, 2],
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/meeting/1/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_meeting(self) -> Meetings:
        """test to delete invalid meeting"""
        """add meeting"""
        url = "/api/meeting/"
        data = {
            "meeting_link": "meeting link",
            "date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "invited_users": [1, 2],
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/meeting/10/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_meetings(self) -> Meetings:
        """test to get all meetings"""
        url = "/api/meeting/"
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_meeting(self) -> Meetings:
        """update meetings"""
        url = "/api/meeting/"
        data = {
            "meeting_link": "meeting link",
            "date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "invited_users": [1, 2],
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/meeting/1/"
        data = {
            "meeting_link": "updated meeting link",
            "date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "invited_users": [1, 2],
        }
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, 202)

    def test_update_meeting_invalid_invited_user(self) -> Meetings:
        """update meeting"""
        url = "/api/meeting/"
        data = {
            "meeting_link": "meeting link",
            "date": {"year": 2022, "month": 9, "day": 8, "hour": 16, "minute": 24},
            "invited_users": [1, 2],
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/meeting/1/"
        data = {"invited_users": [-1]}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_meeting_invalid_date_format(self) -> Meetings:
        """create meeting with no date"""
        url = "/api/meeting/"
        data = {
            "meeting_link": "meeting link",
            "date": "2022-08-23:25p0",
            "invited_users": [1, 2],
        }
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
