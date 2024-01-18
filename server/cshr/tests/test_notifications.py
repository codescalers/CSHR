from rest_framework import status
from server.cshr.models.users import User
from server.cshr.models.office import Office
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase, APIClient


client = APIClient()


class NotificationsTests(APITestCase):
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

    def test_get_notifications_user_authorized(self):
        """get notifications"""
        url = "/api/notifications/"
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notifications_admin_authorized(self):
        """get notifications"""
        url = "/api/notifications/"
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_admin
        )
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notifications_team_lead_authorized(self):
        """get notifications"""
        url = "/api/notifications/"
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_team_lead
        )
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
