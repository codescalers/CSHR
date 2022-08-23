from rest_framework.test import APITestCase
from django.urls import reverse
from ..models.skills import Skills
from rest_framework import status


def createTmp(self):
    """function to create tmp record"""
    url = reverse("skill")
    data = {"name": "testCase"}
    self.client.post(url, data, format="json")


class SkillTests(APITestCase):
    def test_create_skill(self):
        """test ability of creating a new skill"""

        url = reverse("skill")
        data = {"name": "testCase"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skills.objects.count(), 1)

    def test_create_evaluation_error(self):
        """test ability to detect error when creating a new skill"""

        url = reverse("skill")
        data = {"name": "testCase"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_skills(self):

        createTmp(self)
        """create a new record"""
        url = reverse("skill")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "skills found")

    def test_get_all_skill_error(self):
        """test ability to return not found if data base is empty"""
        url = reverse("skill")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_skill_by_id(self):

        createTmp(self)
        """create a new record"""
        url = f"/api/skill/{Skills.objects.get().id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_skill(self):
        """test ability to update record"""

        createTmp(self)
        """create a new record"""
        update_url = f"/api/skill/{Skills.objects.get().id}/"
        response = self.client.patch(update_url, {"name": "updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(Skills.objects.get().name, "updated")

    def test_update_skill_partially(self):

        createTmp(self)
        """create a new record"""

        update_url = f"/api/skill/{Skills.objects.get().id}/"
        response = self.client.patch(update_url, {"name": "updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(Skills.objects.get().name, "updated")

    def test_update_skill_error(self):
        """test update request error: not found"""

        update_url = f"/api/skill/{65}/"
        response = self.client.patch(update_url, {"name": "updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_skill_error1(self):
        """test update request with empty body"""

        createTmp(self)
        """create a new record"""

        update_url = f"/api/skill/{Skills.objects.get().id}/"
        response = self.client.patch(update_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_skill(self):
        # '''test delete record by id'''

        createTmp(self)
        """create a new record"""

        delete_url = f"/api/skill/{Skills.objects.get().id}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Skills.objects.count(), 0)

    def test_delete_evaluation_error(self):
        """test delete record not found response"""
        delete_url = "/api/skill/9/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
