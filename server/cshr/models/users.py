""" database user model """
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AnonymousUser

from typing import Any, Union

from server.cshr.models.abstracts import TimeStamp
from server.cshr.models.office import Office
from server.cshr.utils.dummy_data import create_locations, create_users, create_vacation_balance
from server.cshr.utils.generate import generate_random_color

class TEAM(models.TextChoices):
    """enum class for team options"""
    BusinessDevelopment = "Business Development"
    Development = "Development"
    HRAndFinance = "HR & Finance"
    QA = "QA"
    Marketing = "Marketing"
    Operations = "Operations"
    Support = "Support"


class USER_TYPE(models.TextChoices):
    """types of users"""

    # User-Admin-supervisor
    ADMIN = "Admin", "admin"
    USER = "User", "user"
    SUPERVISOR = "Supervisor", "supervisor"


class GENDER_TYPE(models.TextChoices):
    """gender of users"""

    MALE = "Male", "male"
    FEMALE = "Female", "female"


class CshrBaseUserManger(BaseUserManager):
    """this is the main class for user manger"""

    def create_user(self, email: str, password: str) -> "User":
        """DMC method to create user"""
        if not email:
            raise ValueError("Users must have an email address")

        # Create locations and dummey values to avoid errors after migrating the database, the admins should update it later. 
        create_locations()
        create_vacation_balance()

        from server.components import config
        if config("DJANGO_DEBUG") == "ON":
            create_users()

        user = self.model(
            email=self.normalize_email(email),
            birthday=datetime.datetime.now(),
            location=Office.objects.get(id=2), # Egypt office takes id 2
            user_type=USER_TYPE.ADMIN,
            first_name="Codescalers",
            last_name="Admin",
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str):
        """create superuser"""
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UserSkills(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class User(AbstractBaseUser, TimeStamp):
    """main user model"""

    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    image = models.ImageField(upload_to="profile_image/", null=True, blank=True)
    background_color = models.CharField(max_length=10, default=generate_random_color)
    email = models.EmailField(max_length=45, unique=True)
    mobile_number = models.CharField(max_length=15)
    telegram_link = models.CharField(max_length=100)
    birthday = models.DateField()
    team = models.CharField(max_length=20, choices=TEAM.choices)
    salary = models.JSONField(default=dict)
    location = models.ForeignKey(Office, on_delete=models.CASCADE)
    skills = models.ManyToManyField(
        UserSkills,
        related_name="skills",
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE.choices)
    gender = models.CharField(max_length=20, choices=GENDER_TYPE.choices)
    social_insurance_number = models.CharField(max_length=45)
    address = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)
    USERNAME_FIELD = "email"
    reporting_to = models.ManyToManyField("User", blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CshrBaseUserManger()

    @property
    def full_name(self) -> str:
        "return the user's full name"
        return "%s %s" % (self.first_name.title(), self.last_name.title())

    def has_perm(
        self, perm: str, obj: Union[models.Model, AnonymousUser, None] = None
    ) -> bool:
        """For checking permissions. to keep it simple all admin have ALL permissions"""
        return self.is_admin

    @staticmethod
    def has_module_perms(app_label: Any) -> bool:
        """Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)"""
        return True

    def __str__(self) -> str:
        return f"{self.email}"
