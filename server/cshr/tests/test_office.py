from rest_framework.test import APITestCase
from django.urls import reverse
from ..models.office import Office
from rest_framework import status
from server.cshr.models.users import User


def createTmp():

    """function to create tmp record"""

    Office.objects.create(name="testOffice", country="testCountry")


class OfficeTests(APITestCase):
    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")

        User.objects.create(
            first_name="sting",
            last_name="strig",
            telegram_link="sting",
            email="user1@example.com",
            birthday="2022-08-24",
            mobile_number="sring",
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
        url = "/api/auth/login/"
        data = {"email": "user1@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.results["data"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = "/api/auth/login/"
        data = {"email": "user2@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.results["data"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = "/api/auth/login/"
        data = {"email": "user3@example.com", "password": "string"}
        response = self.client.post(url, data, format="json")
        return response.results["data"]["access_token"]

    """test post method"""

    def test_create_office_by_admin(self):
        """test ability of creating a new office by admin"""
        url = reverse("office")
        data = {"name": "testCase", "country": "testCase"}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Office.objects.last().name, "testCase")

    def test_create_office_by_supervisor(self):
        """test unauthorized  office creation by supervisor"""
        url = reverse("office")
        data = {"name": "testCase1", "country": "testCase1"}
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_office_by_user(self):
        """test unauthorized  office creation by user"""
        url = reverse("office")
        data = {"name": "testCase2", "country": "testCase2"}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_office_by_unauthenticated_user(self):
        """test unauthorized  office creation by unauthenticated user"""
        url = reverse("office")
        data = {"name": "testCase2", "country": "testCase2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """test get method"""

    def test_get_all_office_by_admin(self):
        """test list offices by admin"""
        createTmp()
        """create a new record"""
        url = reverse("office")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.results["message"], "Offices found")

    def test_get_all_office_by_supervisor(self):
        """test list offices by supervisor"""
        createTmp()
        """create a new record"""
        url = reverse("office")
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.results["message"], "Offices found")

    def test_get_all_office_by_user(self):
        """test list offices by user"""
        createTmp()
        """create a new record"""
        url = reverse("office")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.results["message"], "Offices found")

    def test_get_all_office_by_unauthenticated_user(self):
        """test list offices by unauthenticated user"""
        createTmp()
        """create a new record"""
        url = reverse("office")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_office_empty_list(self):
        """test ability to return empty list if database is empty"""
        url = reverse("office")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_office_by_id(self):
        """test get by id with admin credentials"""
        createTmp()
        """create a new record"""
        url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supervisor_get_office_by_id(self):
        """test get by id with supervisor credentials"""
        createTmp()
        """create a new record"""
        url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_office_by_id(self):
        """test get by id with user credentials"""
        createTmp()
        """create a new record"""
        url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_get_office_by_id(self):
        """test get by id with no credentials"""
        createTmp()
        """create a new record"""
        url = f"/api/office/{Office.objects.last().id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """test put methods"""

    def test_admin_update_office(self):
        """test ability to update record with admin credentials"""
        createTmp()
        """create a new record"""
        update_url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.put(
            update_url, {"name": "updatedByAdmin", "country": "updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Office.objects.last().name, "updatedByAdmin")
        self.assertEqual(Office.objects.last().country, "updated")

    def test_supervisor_update_office(self):
        """test ability to update record with supervisor credentials"""
        createTmp()
        """create a new record"""
        update_url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.put(
            update_url,
            {"name": "updatedBySupervisor", "country": "updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Office.objects.last().name, "updatedBySupervisor")
        self.assertEqual(Office.objects.last().country, "updated")

    def test_user_update_office(self):
        """test unauthorized  update record with user credentials"""
        createTmp()
        """create a new record"""
        update_url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.put(
            update_url, {"name": "updatedByUser", "country": "updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_update_office(self):
        """test unauthorized  update record with no credentials"""
        createTmp()
        """create a new record"""
        update_url = f"/api/office/{Office.objects.last().id}/"
        response = self.client.put(
            update_url,
            {"name": "updatedByUnauthenticated", "country": "updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_office_partially(self):
        """update office record partially with admin credentials"""
        createTmp()
        """create a new record"""

        update_url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.put(
            update_url, {"name": "updatedPartially"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_update_not_exists_office(self):
        """test update request error: not found -- with admin credentials"""
        createTmp()
        """create a new record"""

        update_url = f"/api/office/{65}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.put(
            update_url, {"name": "updated", "country": "updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_supervisor_update_not_exists_office(self):
        """test update request error: not found -- with supervisor credentials"""
        createTmp()
        """create a new record"""

        update_url = f"/api/office/{65}/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.put(
            update_url, {"name": "updated", "country": "updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_update_not_exists_office(self):
        """test user update request error: unauthorized -- with user credentials"""
        createTmp()
        """create a new record"""

        update_url = f"/api/office/{65}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.put(
            update_url, {"name": "updated", "country": "updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_update_not_exists_office(self):
        """test user update request error: forbidden -- with no credentials"""
        createTmp()
        """create a new record"""

        update_url = f"/api/office/{65}/"
        response = self.client.put(
            update_url, {"name": "updated", "country": "updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_update_office_bad_request(self):
        """test update request with empty body"""
        createTmp()
        """create a new record"""
        update_url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.put(update_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_delete_office(self):
        """test delete record by id with admin credentials"""
        createTmp()
        """create a new record"""
        count = Office.objects.count()
        delete_url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Office.objects.count(), count - 1)

    def test_supervisor_delete_office(self):
        """test unauthorized delete record by id with supervisor credentials"""
        createTmp()
        """create a new record"""
        count = Office.objects.count()
        delete_url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Office.objects.count(), count)

    def test_user_delete_office(self):
        """test unauthorized delete record by id with supervisor credentials"""
        createTmp()
        """create a new record"""
        count = Office.objects.count()
        delete_url = f"/api/office/{Office.objects.last().id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Office.objects.count(), count)

    def test_unauthenticated_delete_office(self):
        """test delete record by id with no credentials"""
        createTmp()
        """create a new record"""
        count = Office.objects.count()
        delete_url = f"/api/office/{Office.objects.last().id}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Office.objects.count(), count)
