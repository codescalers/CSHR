""" database user model """
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AnonymousUser

from typing import Any, Union

from server.cshr.models.abstracts import TimeStamp
from server.cshr.models.office import Office


class TEAM(models.TextChoices):
    """enum class for team options"""

    # Dev-QA-Ops-Marketing-Management-Accounting

    DEV = "Development"
    QA = "Quality assurance"
    OPS = "Operations"
    MARKETING = "Marketing"
    MANAGEMENT = "Management"
    ACCOUNTING = "Accounting"


class USER_TYPE(models.TextChoices):
    """types of users"""

    # User-Admin-supervisor
    ADMIN = "Admin", "admin"
    USER = "User", "user"
    SUPERVISOR = "Supervisor", "supervisor"


class CshrBaseUserManger(BaseUserManager):
    """this is the main class for user manger"""

    def create_user(self, email: str, password: str) -> "User":
        """DMC method to create user"""
        if not email:
            raise ValueError("Users must have an email address")
        office, created = Office.objects.get_or_create(
            name="Codescalers", country="Egypt"
        )
        user = self.model(
            email=self.normalize_email(email),
            birthday=datetime.datetime.now(),
            location=office,
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


class User(AbstractBaseUser, TimeStamp):
    """main user model"""

    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    image = models.ImageField()
    email = models.EmailField(max_length=45, unique=True)
    mobile_number = models.CharField(max_length=15)
    telegram_link = models.CharField(max_length=100)
    birthday = models.DateField()
    team = models.CharField(max_length=20, choices=TEAM.choices)
    salary = models.JSONField(default=dict)
    location = models.ForeignKey(Office, on_delete=models.CASCADE)
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE.choices)
    USERNAME_FIELD = "email"
    reporting_to = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
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
