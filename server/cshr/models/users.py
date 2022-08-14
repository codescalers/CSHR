""" database user model """

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from server.cshr.models.abstracts import TimeStamp
from server.cshr.models.office import Office
from server.cshr.models.skills import Skills


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


class User(AbstractBaseUser, TimeStamp):
    """main user model"""

    USERNAME_FIELD = "Email"
    FirstName = models.CharField(max_length=45)
    LastName = models.CharField(max_length=45)
    Email = models.EmailField(max_length=45)
    MobileNumber = models.CharField(max_length=15)
    TelegramLink = models.CharField(max_length=100)
    Birthday = models.DateField()
    Team = models.CharField(
        max_length=20, choices=TEAM.choices
    )
    Salary = models.JSONField(default=dict)
    Location_id = models.ForeignKey(Office, on_delete=models.CASCADE)
    Skills_ids = models.ManyToManyField(
        Skills,
        related_name="skills",

    )
    User_type = models.CharField(
        max_length=20,
        choices=USER_TYPE.choices
    )
