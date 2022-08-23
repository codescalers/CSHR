from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from ..models.office import Office
from rest_framework import status


def createTmp(self):

    """function to create tmp record"""
    data = {"name": "testCase", "country": "testCase"}
    post_url = reverse("office")
    self.client.post(post_url, data, format="json")


class OfficeTests(APITestCase):
    def test_create_office(self):
        """test ability of creating a new office"""
        url = reverse("office")
        data = {"name": "testCase", "country": "testCase"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Office.objects.count(), 1)
        self.assertEqual(Office.objects.get().name, "testCase")

    def test_create_office_error(self):
        """test ability to detect error when creating a new office"""
        url = reverse("office")
        data = {"country": "testCase"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_office(self):

        createTmp(self)
        """create a new record"""
        url = reverse("office")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Offices found")

    def test_get_all_office_error(self):
        """test ability to return not found if data base is empty"""
        url = reverse("office")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_office_by_id(self):
        createTmp(self)
        """create a new record"""
        url = f"/api/office/{Office.objects.get().id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_office(self):
        """test ability to update record"""
        createTmp(self)
        """create a new record"""
        update_url = f"/api/office/{Office.objects.get().id}/"
        response = self.client.patch(
            update_url, {"name": "updated", "country": "updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Office.objects.get().name, "updated")
        self.assertEqual(Office.objects.get().country, "updated")

    def test_update_office_partially(self):
        createTmp(self)
        """create a new record"""

        update_url = f"/api/office/{Office.objects.get().id}/"
        response = self.client.patch(update_url, {"name": "updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Office.objects.get().name, "updated")
        self.assertEqual(Office.objects.get().country, "testCase")

    def test_update_office_error(self):
        """test update request error: not found"""
        data = {"name": "testCase", "country": "testCase"}
        createTmp(self)
        """create a new record"""

        update_url = f"/api/office/{65}/"
        response = self.client.patch(
            update_url, {"name": "updated", "country": "updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_office_error1(self):
        """test update request with empty body"""
        createTmp(self)
        """create a new record"""

        update_url = f"/api/office/{Office.objects.get().id}/"
        response = self.client.patch(update_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_office(self):
        # '''test delete record by id'''
        createTmp(self)
        """create a new record"""

        delete_url = f"/api/office/{Office.objects.get().id}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Office.objects.count(), 0)

    def test_delete_office_error(self):
        """test delete record not found response"""
        delete_url = f"/api/office/9/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
