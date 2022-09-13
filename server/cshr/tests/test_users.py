from rest_framework import status
from rest_framework.test import APITestCase
from server.cshr.models.company_properties import CompanyProperties
from server.cshr.models.evaluations import UserEvaluations
from server.cshr.models.training_courses import TrainingCourses
from server.cshr.models.users import User, UserSkills
from server.cshr.models.office import Office
from django.contrib.auth.hashers import make_password


class GeneralViewUserProfileTests(APITestCase):
    "The view of user profiles for all types of users"

    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")
        Office.objects.create(name="testOffice2", country="testCountry2")
        react = UserSkills.objects.create(name="react")
        sql = UserSkills.objects.create(name="sql")

        admin = User.objects.create(
            first_name="Jane",
            last_name="Brown",
            gender="Male",
            telegram_link="@janebrown",
            email="jane@gmail.com",
            birthday="1998-08-24",
            mobile_number="+201234567890",
            location=office,
            password=make_password("adminpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Admin",
            social_insurance_number="086 858 276",
            image="profile_image/default.png",
        )
        admin.skills.add(react)
        admin.skills.add(sql)
        TrainingCourses.objects.create(
            user=admin,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/M683GBLNBAG",
        )
        TrainingCourses.objects.create(
            user=admin,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/AN9NHYDB990",
        )
        CompanyProperties.objects.create(name="computer", user=admin)
        UserEvaluations.objects.create(
            user=admin, link="https://evaluation1", quarter="1 : 3", score=30
        )

        user = User.objects.create(
            first_name="John",
            last_name="Blake",
            gender="Male",
            telegram_link="@johnblake",
            email="john@outlook.com",
            birthday="2000-12-30",
            mobile_number="+201012345678",
            location=office,
            password=make_password("userpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="User",
            social_insurance_number="046 454 286",
            image="profile_image/default.png",
        )
        user.skills.add(react)
        user.skills.add(sql)
        user.reporting_to.set(
            [
                admin.id,
            ]
        )
        TrainingCourses.objects.create(
            user=user,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/BHGJFT7778",
        )
        TrainingCourses.objects.create(
            user=user,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/HBHJJ77H3L",
        )
        CompanyProperties.objects.create(name="computer", user=user)
        UserEvaluations.objects.create(
            user=user, link="https://evaluation2", quarter="1 : 3", score=30
        )

        supervisor = User.objects.create(
            first_name="Sarah",
            last_name="Poland",
            gender="Male",
            telegram_link="@sarahpoland",
            email="sarah@hotmail.com",
            birthday="1996-03-12",
            mobile_number="+201123456789",
            location=office,
            password=make_password("superpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Supervisor",
            social_insurance_number="121 212 121",
            image="profile_image/default.png",
        )
        supervisor.reporting_to.set(
            [
                admin.id,
            ]
        )
        supervisor.skills.add(react)
        supervisor.skills.add(sql)
        TrainingCourses.objects.create(
            user=supervisor,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/HGYFT99JI3",
        )
        TrainingCourses.objects.create(
            user=supervisor,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/KY55GG0OQ1",
        )
        CompanyProperties.objects.create(name="computer", user=supervisor)
        UserEvaluations.objects.create(
            user=supervisor, link="https://evaluation3", quarter="1 : 3", score=30
        )

        self.access_token_admin = self.get_token_admin()
        self.access_token_user = self.get_token_user()
        self.access_token_supervisor = self.get_token_supervisor()

    def get_token_admin(self):
        """Get token for admin user."""
        url = "/api/auth/login/"
        data = {"email": "jane@gmail.com", "password": "adminpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = "/api/auth/login/"
        data = {"email": "john@outlook.com", "password": "userpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = "/api/auth/login/"
        data = {"email": "sarah@hotmail.com", "password": "superpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def test_get_all_users_User(self):
        """a user can view specific fields of all other users.
        can view: Full name, profile picture,birthday,
        Telegram, email address, Joining date, Location (which office), Reporting to, UserSkills,
        trainings and courses achieved and link to certificates (if available)"""
        """cannot view: salary,  Mobile number, Social insurance number, Team, Company properties, evaluation"""

        url = "/api/users/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.data["data"][1]["full_name"], "John Blake")
        self.assertEqual(response.data["data"][1]["birthday"], "2000-12-30")
        self.assertEqual(response.data["data"][1]["telegram_link"], "@johnblake")
        self.assertEqual(response.data["data"][1]["email"], "john@outlook.com")
        self.assertEqual(response.data["data"][1]["location"], 1)
        self.assertEqual(
            response.data["data"][1]["reporting_to"],
            [
                1,
            ],
        )
        self.assertEqual(response.data["data"][1]["skills"], [1, 2])
        self.assertEqual(
            response.data["data"][1]["user_certificates"][0]["name"],
            "Meta Back-End Developer",
        )
        self.assertEqual(response.data["data"][1].get("mobile_number"), None)
        self.assertEqual(response.data["data"][1].get("social_insurance_number"), None)
        self.assertEqual(response.data["data"][1].get("team"), "Development")
        self.assertEqual(response.data["data"][1].get("user_company_properties"), None)
        self.assertEqual(response.data["data"][1].get("user_evaluation"), None)
        self.assertEqual(response.data["data"][1].get("salary"), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_user(self):
        """a user can view specific fields of any other user
        can view: Full name, profile picture,birthday,
        Telegram, email address, Joining date, Location (which office), Reporting to, UserSkills,
        trainings and courses achieved and link to certificates (if available)"""
        url = "/api/users/2/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url, format="json")
        response = self.client.get(url, format="json")
        self.assertEqual(response.data["data"]["full_name"], "John Blake")
        self.assertEqual(response.data["data"]["birthday"], "2000-12-30")
        self.assertEqual(response.data["data"]["telegram_link"], "@johnblake")
        self.assertEqual(response.data["data"]["email"], "john@outlook.com")
        self.assertEqual(response.data["data"]["location"], 1)
        self.assertEqual(
            response.data["data"]["reporting_to"],
            [
                1,
            ],
        )
        self.assertEqual(response.data["data"]["skills"], [1, 2])
        self.assertEqual(
            response.data["data"]["user_certificates"][0]["name"],
            "Meta Back-End Developer",
        )
        self.assertEqual(response.data["data"].get("mobile_number"), None)
        self.assertEqual(response.data["data"].get("social_insurance_number"), None)
        self.assertEqual(response.data["data"].get("team"), "Development")
        self.assertEqual(response.data["data"].get("user_company_properties"), None)
        self.assertEqual(response.data["data"].get("user_evaluation"), None)
        self.assertEqual(response.data["data"].get("salary"), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_user_not_found(self):
        "a not found response is returned when a wrong id os sent"
        url = "/api/users/4/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SupervisorViewUserProfileTests(APITestCase):
    "The view of supervisor profiles for all types of users"

    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")
        Office.objects.create(name="testOffice2", country="testCountry2")
        react = UserSkills.objects.create(name="react")
        sql = UserSkills.objects.create(name="sql")

        admin = User.objects.create(
            first_name="Jane",
            last_name="Brown",
            gender="Female",
            telegram_link="@janebrown",
            email="jane@gmail.com",
            birthday="1998-08-24",
            mobile_number="+201234567890",
            location=office,
            password=make_password("adminpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Admin",
            social_insurance_number="086 858 276",
            image="profile_image/default.png",
        )
        admin.skills.add(react)
        admin.skills.add(sql)
        TrainingCourses.objects.create(
            user=admin,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/M683GBLNBAG",
        )
        TrainingCourses.objects.create(
            user=admin,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/AN9NHYDB990",
        )
        CompanyProperties.objects.create(name="computer", user=admin)
        UserEvaluations.objects.create(
            user=admin, link="https://evaluation1", quarter="1 : 3", score=30
        )

        user = User.objects.create(
            first_name="John",
            last_name="Blake",
            gender="Male",
            telegram_link="@johnblake",
            email="john@outlook.com",
            birthday="2000-12-30",
            mobile_number="+201012345678",
            location=office,
            password=make_password("userpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="User",
            social_insurance_number="046 454 286",
            image="profile_image/default.png",
        )
        user.reporting_to.set(
            [
                admin.id,
            ]
        )
        user.skills.add(react)
        user.skills.add(sql)
        TrainingCourses.objects.create(
            user=user,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/BHGJFT7778",
        )
        TrainingCourses.objects.create(
            user=user,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/HBHJJ77H3L",
        )
        CompanyProperties.objects.create(name="computer", user=user)
        UserEvaluations.objects.create(
            user=user, link="https://evaluation2", quarter="1 : 3", score=30
        )

        supervisor = User.objects.create(
            first_name="Sarah",
            last_name="Poland",
            gender="Female",
            telegram_link="@sarahpoland",
            email="sarah@hotmail.com",
            birthday="1996-03-12",
            mobile_number="+201123456789",
            location=office,
            password=make_password("superpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Supervisor",
            social_insurance_number="121 212 121",
            image="profile_image/default.png",
        )
        supervisor.reporting_to.set(
            [
                admin.id,
            ]
        )
        supervisor.skills.add(react)
        supervisor.skills.add(sql)
        TrainingCourses.objects.create(
            user=supervisor,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/HGYFT99JI3",
        )
        TrainingCourses.objects.create(
            user=supervisor,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/KY55GG0OQ1",
        )
        CompanyProperties.objects.create(name="computer", user=supervisor)
        UserEvaluations.objects.create(
            user=supervisor, link="https://evaluation3", quarter="1 : 3", score=30
        )

        self.access_token_admin = self.get_token_admin()
        self.access_token_user = self.get_token_user()
        self.access_token_supervisor = self.get_token_supervisor()

    def get_token_admin(self):
        """Get token for admin user."""
        url = "/api/auth/login/"
        data = {"email": "jane@gmail.com", "password": "adminpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = "/api/auth/login/"
        data = {"email": "john@outlook.com", "password": "userpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = "/api/auth/login/"
        data = {"email": "sarah@hotmail.com", "password": "superpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def test_get_all_users_supervisor(self):
        """a supervisor can view specific all fields of all other users except salary"""
        url = "/api/users/supervisor/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data["data"]), 3)
        self.assertEqual(response.data["data"][1]["full_name"], "John Blake")
        self.assertEqual(
            response.data["data"][1]["image"],
            "http://testserver/profile_image/default.png",
        )
        self.assertEqual(response.data["data"][1]["birthday"], "2000-12-30")
        self.assertEqual(response.data["data"][1]["telegram_link"], "@johnblake")
        self.assertEqual(response.data["data"][1]["email"], "john@outlook.com")
        self.assertEqual(response.data["data"][1]["location"], 1)
        self.assertEqual(
            response.data["data"][1]["reporting_to"],
            [
                1,
            ],
        )
        self.assertEqual(response.data["data"][1]["skills"], [1, 2])
        self.assertEqual(
            response.data["data"][1]["user_certificates"][0]["name"],
            "Meta Back-End Developer",
        )
        self.assertEqual(response.data["data"][1]["mobile_number"], "+201012345678")
        self.assertEqual(
            response.data["data"][1]["social_insurance_number"], "046 454 286"
        )
        self.assertEqual(response.data["data"][1]["team"], "Development")
        self.assertEqual(
            response.data["data"][1]["user_company_properties"][0]["name"], "computer"
        )
        self.assertEqual(
            response.data["data"][1]["user_evaluation"][0]["link"],
            "https://evaluation2",
        )
        self.assertEqual(response.data["data"][1].get("salary"), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_user_supervisor(self):
        """a supervisor can view all fields of a specific user except salary"""
        url = "/api/users/supervisor/2/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.data["data"]["full_name"], "John Blake")
        self.assertEqual(
            response.data["data"]["image"],
            "http://testserver/profile_image/default.png",
        )
        self.assertEqual(response.data["data"]["birthday"], "2000-12-30")
        self.assertEqual(response.data["data"]["telegram_link"], "@johnblake")
        self.assertEqual(response.data["data"]["email"], "john@outlook.com")
        self.assertEqual(response.data["data"]["location"], 1)
        self.assertEqual(
            response.data["data"]["reporting_to"],
            [
                1,
            ],
        )
        self.assertEqual(response.data["data"]["skills"], [1, 2])
        self.assertEqual(
            response.data["data"]["user_certificates"][0]["name"],
            "Meta Back-End Developer",
        )
        self.assertEqual(response.data["data"]["mobile_number"], "+201012345678")
        self.assertEqual(
            response.data["data"]["social_insurance_number"], "046 454 286"
        )
        self.assertEqual(response.data["data"]["team"], "Development")
        self.assertEqual(
            response.data["data"]["user_company_properties"][0]["name"], "computer"
        )
        self.assertEqual(
            response.data["data"]["user_evaluation"][0]["link"], "https://evaluation2"
        )
        self.assertEqual(response.data["data"].get("salary"), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_normaluser(self):
        """a normal user cannot access any supervisor endpoint"""
        url = "/api/users/supervisor/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_a_user_normaluser(self):
        """a normal user cannot access any supervisor endpoint"""
        url = "/api/users/supervisor/2/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_users_admin(self):
        """an admin cannot access any supervisor endpoint"""
        url = "/api/users/supervisor/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_a_user_admin(self):
        """an admin cannot access any supervisor endpoint"""
        url = "/api/users/supervisor/2/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminViewUserProfileTests(APITestCase):
    """an admin can view all users with all specific fields, update and delete a user"""

    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")
        Office.objects.create(name="testOffice2", country="testCountry2")
        react = UserSkills.objects.create(name="react")
        sql = UserSkills.objects.create(name="sql")

        admin = User.objects.create(
            first_name="Jane",
            last_name="Brown",
            gender="Female",
            telegram_link="@janebrown",
            email="jane@gmail.com",
            birthday="1998-08-24",
            mobile_number="+201234567890",
            location=office,
            password=make_password("adminpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Admin",
            social_insurance_number="086 858 276",
            image="profile_image/default.png",
        )
        admin.skills.add(react)
        admin.skills.add(sql)
        TrainingCourses.objects.create(
            user=admin,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/M683GBLNBAG",
        )
        TrainingCourses.objects.create(
            user=admin,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/AN9NHYDB990",
        )
        CompanyProperties.objects.create(name="computer", user=admin)
        UserEvaluations.objects.create(
            user=admin, link="https://evaluation1", quarter="1 : 3", score=30
        )

        user = User.objects.create(
            first_name="John",
            last_name="Blake",
            gender="Female",
            telegram_link="@johnblake",
            email="john@outlook.com",
            birthday="2000-12-30",
            mobile_number="+201012345678",
            location=office,
            password=make_password("userpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="User",
            social_insurance_number="046 454 286",
            image="profile_image/default.png",
        )
        user.reporting_to.set(
            [
                admin.id,
            ]
        )
        user.skills.add(react)
        user.skills.add(sql)
        TrainingCourses.objects.create(
            user=user,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/BHGJFT7778",
        )
        TrainingCourses.objects.create(
            user=user,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/HBHJJ77H3L",
        )
        CompanyProperties.objects.create(name="computer", user=user)
        UserEvaluations.objects.create(
            user=user, link="https://evaluation2", quarter="1 : 3", score=30
        )

        supervisor = User.objects.create(
            first_name="Sarah",
            last_name="Poland",
            gender="Female",
            telegram_link="@sarahpoland",
            email="sarah@hotmail.com",
            birthday="1996-03-12",
            mobile_number="+201123456789",
            location=office,
            password=make_password("superpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Supervisor",
            social_insurance_number="121 212 121",
            image="profile_image/default.png",
        )
        supervisor.reporting_to.set(
            [
                admin.id,
            ]
        )
        supervisor.skills.add(react)
        supervisor.skills.add(sql)
        TrainingCourses.objects.create(
            user=supervisor,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/HGYFT99JI3",
        )
        TrainingCourses.objects.create(
            user=supervisor,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/KY55GG0OQ1",
        )
        CompanyProperties.objects.create(name="computer", user=supervisor)
        UserEvaluations.objects.create(
            user=supervisor, link="https://evaluation3", quarter="1 : 3", score=30
        )

        self.access_token_admin = self.get_token_admin()
        self.access_token_user = self.get_token_user()
        self.access_token_supervisor = self.get_token_supervisor()

    def get_token_admin(self):
        """Get token for admin user."""
        url = "/api/auth/login/"
        data = {"email": "jane@gmail.com", "password": "adminpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = "/api/auth/login/"
        data = {"email": "john@outlook.com", "password": "userpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = "/api/auth/login/"
        data = {"email": "sarah@hotmail.com", "password": "superpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def test_get_all_users(self):
        "an admin can view all fields a supervisor can view of all users in addition to salary"
        """can view: Full name, profile picture,birthday,
        Telegram, email address, Joining date, Location (which office), Reporting to, UserSkills,
        trainings and courses achieved and link to certificates (if available), salary,
        Mobile number, Social insurance number, Team, Company properties, evaluation"""
        url = "/api/users/admin/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data["data"]), 3)
        self.assertEqual(response.data["data"][1]["full_name"], "John Blake")
        self.assertEqual(
            response.data["data"][1]["image"],
            "http://testserver/profile_image/default.png",
        )
        self.assertEqual(response.data["data"][1]["birthday"], "2000-12-30")
        self.assertEqual(response.data["data"][1]["telegram_link"], "@johnblake")
        self.assertEqual(response.data["data"][1]["email"], "john@outlook.com")
        self.assertEqual(response.data["data"][1]["location"], 1)
        self.assertEqual(
            response.data["data"][1]["reporting_to"],
            [
                1,
            ],
        )
        self.assertEqual(response.data["data"][1]["skills"], [1, 2])
        self.assertEqual(
            response.data["data"][1]["user_certificates"][0]["name"],
            "Meta Back-End Developer",
        )
        self.assertEqual(response.data["data"][1]["mobile_number"], "+201012345678")
        self.assertEqual(
            response.data["data"][1]["social_insurance_number"], "046 454 286"
        )
        self.assertEqual(response.data["data"][1]["team"], "Development")
        self.assertEqual(
            response.data["data"][1]["user_company_properties"][0]["name"], "computer"
        )
        self.assertEqual(
            response.data["data"][1]["user_evaluation"][0]["link"],
            "https://evaluation2",
        )
        self.assertEqual(response.data["data"][1]["salary"], {"gross": 2000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_user(self):
        "an admin can view all fields of a specific user including salary"
        url = "/api/users/admin/2/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.get(url, format="json")
        self.assertEqual(response.data["data"]["full_name"], "John Blake")
        self.assertEqual(
            response.data["data"]["image"],
            "http://testserver/profile_image/default.png",
        )
        self.assertEqual(response.data["data"]["birthday"], "2000-12-30")
        self.assertEqual(response.data["data"]["telegram_link"], "@johnblake")
        self.assertEqual(response.data["data"]["email"], "john@outlook.com")
        self.assertEqual(response.data["data"]["location"], 1)
        self.assertEqual(
            response.data["data"]["reporting_to"],
            [
                1,
            ],
        )
        self.assertEqual(response.data["data"]["skills"], [1, 2])
        self.assertEqual(
            response.data["data"]["user_certificates"][0]["name"],
            "Meta Back-End Developer",
        )
        self.assertEqual(response.data["data"]["mobile_number"], "+201012345678")
        self.assertEqual(
            response.data["data"]["social_insurance_number"], "046 454 286"
        )
        self.assertEqual(response.data["data"]["team"], "Development")
        self.assertEqual(
            response.data["data"]["user_company_properties"][0]["name"], "computer"
        )
        self.assertEqual(
            response.data["data"]["user_evaluation"][0]["link"], "https://evaluation2"
        )
        self.assertEqual(response.data["data"]["salary"], {"gross": 2000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_user_not_found(self):
        "a not found response is returned when a wrong id os sent"
        url = "/api/users/admin/4/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_all_fields_of_a_user(self):
        "an admin can edit all user fields including location, team, reporting to and salary"
        url = "/api/users/admin/2/"
        data = {
            "email": "user@example.com",
            "telegram_link": "@userexample",
            "birthday": "1981-08-31",
            "social_insurance_number": "123 456 789",
            "location": 2,
            "team": "Marketing",
            "reporting_to": [],
            "salary": {"gross": 9000},
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.put(url, data, format="json")
        getresponse = self.client.get(url, format="json")
        self.assertEqual(response.data["data"]["email"], "user@example.com")
        self.assertEqual(getresponse.data["data"]["salary"], {"gross": 9000})
        self.assertEqual(response.data["data"]["telegram_link"], "@userexample")
        self.assertEqual(
            response.data["data"]["social_insurance_number"], "123 456 789"
        )
        self.assertEqual(response.data["data"]["birthday"], "1981-08-31")
        self.assertEqual(getresponse.data["data"]["reporting_to"], [])
        self.assertEqual(getresponse.data["data"]["team"], "Marketing")
        self.assertEqual(getresponse.data["data"]["location"], 2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_a_user(self):
        "an admin can delete any user"
        url = "/api/users/admin/2/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_admin)
        response = self.client.delete(url, format="json")
        getresponse = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(getresponse.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_users_normaluser(self):
        """a normal user cannot access any adminview endpoint"""
        url = "/api/users/admin/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_a_user_normaluser(self):
        """a normal user cannot access any adminview endpoint"""
        url = "/api/users/admin/2/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_all_fields_of_a_user_normaluser(self):
        """a normal user cannot access any adminview endpoint"""
        url = "/api/users/admin/2/"
        data = {
            "email": "user@example.com",
            "telegram_link": "@userexample",
            "birthday": "1981-08-31",
            "social_insurance_number": "123 456 789",
            "location": 2,
            "team": "Marketing",
            "reporting_to": [],
            "salary": {"gross": 9000},
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_a_user_normaluser(self):
        """a normal user cannot access any adminview endpoint"""
        url = "/api/users/admin/2/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_users_supervisor(self):
        """a supervisor cannot access any adminview endpoint"""
        url = "/api/users/admin/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_a_user_supervisor(self):
        """a supervisor cannot access any adminview endpoint"""
        url = "/api/users/admin/2/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_all_fields_of_a_user_supervisor(self):
        """a supervisor user cannot access any adminview endpoint"""
        url = "/api/users/admin/2/"
        data = {
            "email": "user@example.com",
            "telegram_link": "@userexample",
            "birthday": "1981-08-31",
            "social_insurance_number": "123 456 789",
            "location": 2,
            "team": "Marketing",
            "reporting_to": [],
            "salary": {"gross": 9000},
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_a_user_supervisor(self):
        """a supervisor cannot access any adminview endpoint"""
        url = "/api/users/admin/2/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_supervisor
        )
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SelfViewUserProfileTests(APITestCase):
    """a user can view their own profile with all specific fields and update it"""

    def setUp(self):
        office = Office.objects.create(name="testOffice", country="testCountry")
        Office.objects.create(name="testOffice2", country="testCountry2")
        react = UserSkills.objects.create(name="react")
        sql = UserSkills.objects.create(name="sql")

        admin = User.objects.create(
            first_name="Jane",
            last_name="Brown",
            gender="Female",
            telegram_link="@janebrown",
            email="jane@gmail.com",
            birthday="1998-08-24",
            mobile_number="+201234567890",
            location=office,
            password=make_password("adminpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Admin",
            social_insurance_number="086 858 276",
            image="profile_image/default.png",
        )
        admin.skills.add(react)
        admin.skills.add(sql)
        TrainingCourses.objects.create(
            user=admin,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/M683GBLNBAG",
        )
        TrainingCourses.objects.create(
            user=admin,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/AN9NHYDB990",
        )
        CompanyProperties.objects.create(name="computer", user=admin)
        UserEvaluations.objects.create(
            user=admin, link="https://evaluation1", quarter="1 : 3", score=30
        )

        user = User.objects.create(
            first_name="John",
            last_name="Blake",
            gender="Male",
            telegram_link="@johnblake",
            email="john@outlook.com",
            birthday="2000-12-30",
            mobile_number="+201012345678",
            location=office,
            password=make_password("userpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="User",
            social_insurance_number="046 454 286",
            image="profile_image/default.png",
        )
        user.reporting_to.set(
            [
                admin.id,
            ]
        )
        user.skills.add(react)
        user.skills.add(sql)
        TrainingCourses.objects.create(
            user=user,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/BHGJFT7778",
        )
        TrainingCourses.objects.create(
            user=user,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/HBHJJ77H3L",
        )
        CompanyProperties.objects.create(name="computer", user=user)
        UserEvaluations.objects.create(
            user=user, link="https://evaluation2", quarter="1 : 3", score=30
        )

        supervisor = User.objects.create(
            first_name="Sarah",
            last_name="Poland",
            gender="Female",
            telegram_link="@sarahpoland",
            email="sarah@hotmail.com",
            birthday="1996-03-12",
            mobile_number="+201123456789",
            location=office,
            password=make_password("superpassword"),
            team="Development",
            salary={"gross": 2000},
            user_type="Supervisor",
            social_insurance_number="121 212 121",
            image="profile_image/default.png",
        )
        supervisor.reporting_to.set(
            [
                admin.id,
            ]
        )
        supervisor.skills.add(react)
        supervisor.skills.add(sql)
        TrainingCourses.objects.create(
            user=supervisor,
            name="Meta Back-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/HGYFT99JI3",
        )
        TrainingCourses.objects.create(
            user=supervisor,
            name="Meta Front-End Developer",
            certificate_link="https://www.coursera.org/account/accomplishments/verify/KY55GG0OQ1",
        )
        CompanyProperties.objects.create(name="computer", user=supervisor)
        UserEvaluations.objects.create(
            user=supervisor, link="https://evaluation3", quarter="1 : 3", score=30
        )

        self.access_token_admin = self.get_token_admin()
        self.access_token_user = self.get_token_user()
        self.access_token_supervisor = self.get_token_supervisor()

    def get_token_admin(self):
        """Get token for admin user."""
        url = "/api/auth/login/"
        data = {"email": "jane@gmail.com", "password": "adminpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_user(self):
        """Get token for normal user."""
        url = "/api/auth/login/"
        data = {"email": "john@outlook.com", "password": "userpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def get_token_supervisor(self):
        """Get token for a supervisor user."""
        url = "/api/auth/login/"
        data = {"email": "sarah@hotmail.com", "password": "superpassword"}
        response = self.client.post(url, data, format="json")
        return response.data["data"]["access_token"]

    def test_get_my_profile(self):
        "any user can view all the fields of their profile including salary"
        url = "/api/myprofile/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.data["data"]["full_name"], "John Blake")
        self.assertEqual(
            response.data["data"]["image"],
            "http://testserver/profile_image/default.png",
        )
        self.assertEqual(response.data["data"]["birthday"], "2000-12-30")
        self.assertEqual(response.data["data"]["telegram_link"], "@johnblake")
        self.assertEqual(response.data["data"]["email"], "john@outlook.com")
        self.assertEqual(response.data["data"]["location"], 1)
        self.assertEqual(
            response.data["data"]["reporting_to"][0]["email"], "jane@gmail.com"
        )
        self.assertEqual(response.data["data"]["skills"], [1, 2])
        self.assertEqual(
            response.data["data"]["user_certificates"][0]["name"],
            "Meta Back-End Developer",
        )
        self.assertEqual(response.data["data"]["mobile_number"], "+201012345678")
        self.assertEqual(
            response.data["data"]["social_insurance_number"], "046 454 286"
        )
        self.assertEqual(response.data["data"]["team"], "Development")
        self.assertEqual(
            response.data["data"]["user_company_properties"][0]["name"], "computer"
        )
        self.assertEqual(
            response.data["data"]["user_evaluation"][0]["link"], "https://evaluation2"
        )
        self.assertEqual(response.data["data"]["salary"], {"gross": 2000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_my_profile(self):
        "any user can some fields of their profile"
        url = "/api/myprofile/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user)
        data = {
            "email": "janjoun@example.com",
            "telegram_link": "@janjounexample",
            "birthday": "1981-08-31",
            "social_insurance_number": "123 456 789",
            "mobile_number": "+201093129222",
        }
        response = self.client.put(url, data, format="json")
        getresponse = self.client.get(url, format="json")
        self.assertEqual(getresponse.data["data"]["full_name"], "John Blake")
        self.assertEqual(
            getresponse.data["data"]["image"],
            "http://testserver/profile_image/default.png",
        )
        self.assertEqual(getresponse.data["data"]["birthday"], "1981-08-31")
        self.assertEqual(getresponse.data["data"]["telegram_link"], "@janjounexample")
        self.assertEqual(getresponse.data["data"]["email"], "janjoun@example.com")
        self.assertEqual(getresponse.data["data"]["location"], 1)
        self.assertEqual(
            getresponse.data["data"]["reporting_to"][0]["email"], "jane@gmail.com"
        )
        self.assertEqual(getresponse.data["data"]["skills"], [1, 2])
        self.assertEqual(
            getresponse.data["data"]["user_certificates"][0]["name"],
            "Meta Back-End Developer",
        )
        self.assertEqual(getresponse.data["data"]["mobile_number"], "+201093129222")
        self.assertEqual(
            getresponse.data["data"]["social_insurance_number"], "123 456 789"
        )
        self.assertEqual(getresponse.data["data"]["team"], "Development")
        self.assertEqual(
            getresponse.data["data"]["user_company_properties"][0]["name"], "computer"
        )
        self.assertEqual(
            getresponse.data["data"]["user_evaluation"][0]["link"],
            "https://evaluation2",
        )
        self.assertEqual(getresponse.data["data"]["salary"], {"gross": 2000})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
