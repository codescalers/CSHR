# from rest_framework import status
# from rest_framework.test import APITestCase, APIClient

# from server.cshr.models.users import User
# from server.cshr.models.office import Office
# from server.cshr.models.company_properties import CompanyProperties
# from django.contrib.auth.hashers import make_password


# client = APIClient()


# class CompanyPropertiesTests(APITestCase):
#     def setUp(self):
#         office = Office.objects.create(name="testOffice", country="testCountry")

#         User.objects.create(
#             first_name="Ahmed",
#             last_name="Mohamed",
#             telegram_link="https://t.me/ahmed2",
#             email="ahmed@gmail.com",
#             birthday="1995-08-24",
#             mobile_number="0123456789",
#             password=make_password("ahmedpass"),
#             location=office,
#             team="Development",
#             user_type="Admin",
#         )

#         User.objects.create(
#             first_name="Andrew",
#             last_name="Nassef",
#             telegram_link="https://t.me/andrew",
#             email="andrew@gmail.com",
#             birthday="2001-08-24",
#             mobile_number="010234567",
#             password=make_password("andrewpass"),
#             location=office,
#             team="Development",
#             user_type="User",
#         )

#         User.objects.create(
#             first_name="Helmy",
#             last_name="Bakr",
#             telegram_link="https://t.me/helmy",
#             email="helmy@gmail.com",
#             birthday="2000-08-24",
#             mobile_number="01238512",
#             password=make_password("helmypass"),
#             location=office,
#             team="Development",
#             user_type="Supervisor",
#         )

#         self.access_token_admin = self.get_token_admin()
#         self.access_token_user = self.get_token_user()
#         self.access_token_supervisor = self.get_token_supervisor()

#     def get_token_admin(self):
#         """Get token for admin user."""
#         url = f'{"/api/auth/login/"}'
#         data = {"email": "ahmed@gmail.com", "password": "ahmedpass"}
#         response = self.client.post(url, data, format="json")
#         return response.data["results"]["access_token"]

#     def get_token_user(self):
#         """Get token for normal user."""
#         url = f'{"/api/auth/login/"}'
#         data = {"email": "andrew@gmail.com", "password": "andrewpass"}
#         response = self.client.post(url, data, format="json")
#         return response.data["results"]["access_token"]

#     def get_token_supervisor(self):
#         """Get token for a supervisor user."""
#         url = f'{"/api/auth/login/"}'
#         data = {"email": "helmy@gmail.com", "password": "helmypass"}
#         response = self.client.post(url, data, format="json")
#         return response.data["results"]["access_token"]

#     def test_create_company_properties(self) -> CompanyProperties:
#         url = "/api/company_properties/"
#         data = {
#             "name": "string",
#         }
#         self.headers = client.credentials(
#             HTTP_AUTHORIZATION="Bearer " + self.access_token_user
#         )
#         response = client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_company_properties_no_data(self) -> CompanyProperties:
#         url = "/api/company_properties/"
#         data = {}
#         self.headers = client.credentials(
#             HTTP_AUTHORIZATION="Bearer " + self.access_token_user
#         )
#         response = client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_get_creation_company_properties(self) -> CompanyProperties:
#         """test to get a valid company_properties"""
#         """add company_properties"""
#         url = "/api/company_properties/"
#         data = {
#             "name": "string",
#         }
#         self.headers = client.credentials(
#             HTTP_AUTHORIZATION="Bearer " + self.access_token_user
#         )
#         response = client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         url = "/api/company_properties/1/"
#         response = client.get(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_invalid_company_properties(self) -> CompanyProperties:
#         """test to get a valid company_properties"""
#         """add company_properties"""
#         url = "/api/company_properties/"
#         data = {
#             "name": "string",
#         }
#         self.headers = client.credentials(
#             HTTP_AUTHORIZATION="Bearer " + self.access_token_user
#         )
#         response = client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         url = "/api/company_properties/10/"
#         response = client.get(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_delete_company_properties(self) -> CompanyProperties:
#         """test to delete a valid company_properties"""
#         """add company_properties"""
#         url = "/api/company_properties/"
#         data = {
#             "name": "string",
#         }
#         self.headers = client.credentials(
#             HTTP_AUTHORIZATION="Bearer " + self.access_token_user
#         )
#         response = client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         url = "/api/company_properties/1/"
#         response = client.delete(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_delete_invalid_company_properties(self) -> CompanyProperties:
#         """test to delete invalid compensation"""
#         """add company_properties"""
#         url = "/api/company_properties/"
#         data = {
#             "name": "string",
#         }
#         self.headers = client.credentials(
#             HTTP_AUTHORIZATION="Bearer " + self.access_token_user
#         )
#         response = client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         url = "/api/company_properties/10/"
#         response = client.delete(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_company_properties(self) -> CompanyProperties:
#         """update company_properties"""
#         url = "/api/company_properties/"
#         data = {
#             "name": "string",
#         }
#         response = client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         url = "/api/company_properties/1/"
#         data = {"user": 1}
#         self.headers = client.credentials(
#             HTTP_AUTHORIZATION="Bearer " + self.access_token_user
#         )
#         response = client.put(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
