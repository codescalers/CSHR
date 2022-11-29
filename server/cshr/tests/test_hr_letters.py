from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from server.cshr.models.users import User
from server.cshr.models.office import Office
from server.cshr.models.hr_letters import HrLetters
from django.contrib.auth.hashers import make_password

client = APIClient()


class HrLetterTests(APITestCase):
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
        return response.data["results"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = f'{"/api/auth/login/"}'
        data = {"email": "andrew@gmail.com", "password": "andrewpass"}
        response = self.client.post(url, data, format="json")
        return response.data["results"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = f'{"/api/auth/login/"}'
        data = {"email": "helmy@gmail.com", "password": "helmypass"}
        response = self.client.post(url, data, format="json")
        return response.data["results"]["access_token"]

    def test_create_hr_letter(self) -> HrLetters:
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_hr_letter_no_address(self) -> HrLetters:
        url = "/api/hr_letters/"
        data = {}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_certain_hr_letters(self) -> HrLetters:
        """test to get a valid hr letter"""
        """add hr letter"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/1/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_hr_letter(self) -> HrLetters:
        """test to get a valid hr letter"""
        """add hr letter"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/10/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_certain_hr_letters(self) -> HrLetters:
        """test to delete a valid hr letter"""
        """add hr letter"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/1/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_hr_letters(self) -> HrLetters:
        """test to delete invalid hr letter"""
        """add hr letter"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/10/"
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_hr_letters(self) -> HrLetters:
        """test to get all hr letters"""
        url = "/api/hr_letters/"
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_hr_letter(self) -> HrLetters:
        """update hr letter"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/edit/1/"
        data = {"applying_user": 1}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, 202)

    def test_update_hr_letter_non_authorized(self) -> HrLetters:
        """update hr letter"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/edit/1/"
        data = {"applying_user": 1}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_update_hr_letter_invalid_user_id(self) -> HrLetters:
        """update hr letter"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        response = client.post(url, data, format="json")
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/edit/1/"
        data = {"applying_user": -1}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_hr_letters_for_user_with_data(self) -> HrLetters:
        """add hr letter"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        response = client.post(url, data, format="json")
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/user/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_hr_letters_for_user_without_data(self) -> HrLetters:
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        url = "/api/hr_letters/user/"
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_hr_letter_for_unauthorized_user(self) -> HrLetters:
        """add hr letter request"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/approve/1/"
        response = client.put(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_hr_letter_for_unauthorized_user(self) -> HrLetters:
        """add hr letter request"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/reject/1/"
        response = client.put(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_hr_letter_for_admin_auth(self) -> HrLetters:
        """add hr letter request"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_admin
        )
        url = "/api/hr_letters/approve/1/"
        response = client.put(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_reject_hrletter_for_supervisor_auth(self) -> HrLetters:
        """add hr letter request"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/reject/1/"
        response = client.put(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_invalid_hrletter(self) -> HrLetters:
        """add hr letter request"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = "/api/hr_letters/reject/-1/"
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_admin
        )
        response = client.put(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_accept_invalid_hr_letter(self) -> HrLetters:
        """add hr letter request"""
        url = "/api/hr_letters/"
        data = {"addresses": "testing addr"}
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user
        )
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.headers = client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_admin
        )
        url = "/api/hr_letters/approve/-1/"
        response = client.put(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
