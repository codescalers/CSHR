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

    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    mobile_number = models.CharField(max_length=15)
    telegram_link = models.CharField(max_length=100)
    birthday = models.DateField()
    team = models.CharField(max_length=20, choices=TEAM.choices)
    salary = models.JSONField(default=dict)
    location = models.ForeignKey(Office, on_delete=models.CASCADE)
    skills = models.ManyToManyField(
        Skills,
        related_name="skills",
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE.choices)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property 
    def full_name(self):
        "return the user's full name"
        return '%s %s' % (self.first_name, self.last_name)

