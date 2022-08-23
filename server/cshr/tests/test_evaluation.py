from rest_framework.test import APITestCase
from django.urls import reverse
from ..models.evaluations import Evaluations
from ..models.users import User
from ..models.office import Office
from rest_framework import status


def create_baseDate():
    """create instance of user and office to resolve ForeignKeys"""
    officeTest = Office.objects.create(name="officeTest", country="officeTest")
    userTest = User(
        first_name="omar",
        last_name="test",
        image="tmp",
        email="omnar@tmp.com",
        mobile_number="2341343",
        telegram_link="tmp",
        birthday="2000-12-10",
        team="Development",
        location=officeTest,
        user_type="Admin",
    )
    userTest.save()


def createTmpEvaluation(self):
    """function to create tmp record"""
    url = reverse("evaluation")
    data = {"user": 1, "link": "testCase"}
    self.client.post(url, data, format="json")


class EvaluationTests(APITestCase):
    def test_create_evaluation(self):
        """test ability of creating a new evaluation"""
        create_baseDate()
        url = reverse("evaluation")
        data = {"user": 1, "link": "testCase"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Evaluations.objects.count(), 1)
        self.assertEqual(Evaluations.objects.get().user.id, 1)

    def test_create_evaluation_error(self):
        """test ability to detect error when creating a new evaluation"""
        create_baseDate()
        url = reverse("evaluation")
        data = {"link": "testCase"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_office(self):

        create_baseDate()
        createTmpEvaluation(self)
        """create a new record"""
        url = reverse("evaluation")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "evaluations found")

    def test_get_all_evaluation_error(self):
        """test ability to return not found if data base is empty"""
        url = reverse("evaluation")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_evaluation_by_id(self):
        create_baseDate()
        createTmpEvaluation(self)
        """create a new record"""
        url = f"/api/evaluation/{Evaluations.objects.get().id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_evaluation(self):
        """test ability to update record"""
        create_baseDate()
        createTmpEvaluation(self)
        """create a new record"""
        update_url = f"/api/evaluation/{Evaluations.objects.get().id}/"
        response = self.client.patch(
            update_url, {"user": 1, "link": "updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Evaluations.objects.get().user.id, 1)
        self.assertEqual(Evaluations.objects.get().link, "updated")

    def test_update_evaluation_partially(self):
        create_baseDate()
        createTmpEvaluation(self)
        """create a new record"""

        update_url = f"/api/evaluation/{Evaluations.objects.get().id}/"
        response = self.client.patch(update_url, {"link": "updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Evaluations.objects.get().user.id, 1)
        self.assertEqual(Evaluations.objects.get().link, "updated")

    def test_update_evaluation_error(self):
        """test update request error: not found"""

        update_url = f"/api/evaluation/{65}/"
        response = self.client.patch(update_url, {"link": "updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_evaluation_error1(self):
        """test update request with empty body"""
        create_baseDate()
        createTmpEvaluation(self)
        """create a new record"""

        update_url = f"/api/evaluation/{Evaluations.objects.get().id}/"
        response = self.client.patch(update_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_evaluation(self):
        # '''test delete record by id'''
        create_baseDate()
        createTmpEvaluation(self)
        """create a new record"""

        delete_url = f"/api/evaluation/{Evaluations.objects.get().id}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Evaluations.objects.count(), 0)

    def test_delete_evaluation_error(self):
        """test delete record not found response"""
        delete_url = "/api/evaluation/9/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
