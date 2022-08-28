from rest_framework.test import APITestCase
from server.cshr.models.users import User
from server.cshr.models.office import Office


class AdminViewUserProfileTests(APITestCase):
    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")
        Office.objects.create(name="testOffice2", country="testCountry2")

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
            salary={"gross": 2000},
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
            salary={"gross": 2000},
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
            salary={"gross": 2000},
            user_type="Supervisor",
        )

        self.access_token_admin = self.get_token_admin()
        self.access_token_user = self.get_token_user()
        self.access_token_supervisor = self.get_token_supervisor()

    def get_token_admin(self):
        """Get token for admin user."""
        url = 'f{"/api/auth/login/"}'
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

    # def test_get_all_users(self):
    #     "an admin can view all fields of all users including salary"
    #     url = "/api/users/adminView/"
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
    #     response = self.client.get(url, format="json")
    #     self.assertEqual(len(response.data["data"]), 3)
    #     self.assertEqual(response.data["data"][1]["salary"], {"gross": 2000})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_a_user(self):
    #     "an admin can view all fields of a specific user including salary"
    #     url = "/api/users/adminView/1/"
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
    #     response = self.client.get(url, format="json")
    #     self.assertEqual(response.data["data"]["salary"], {"gross": 2000})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_a_user_not_found(self):
    #     "a not found response is returned when a wrong id os sent"
    #     url = "/api/users/adminView/4/"
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
    #     response = self.client.get(url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
