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
    reporting_to= models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    social_insurance_number = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    image = models.ImageField(upload_to="profile_image")
    email = models.EmailField(max_length=45, unique=True)
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
    USERNAME_FIELD = "email"

    @property
    def full_name(self) -> str:
        "return the user's full name"
        return "%s %s" % (self.first_name.title(), self.last_name.title())

    def __str__(self) -> str:
        return f"{self.email}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-first_name', '-last_name']
        get_latest_by = 'created_at'
