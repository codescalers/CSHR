""" database user model """

from typing import Any, Union
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AnonymousUser

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


class ChsrBaseUserManger(BaseUserManager):
    """This is the main class for user manger"""

    def create_user(self, email: str, password: str) -> "User":
        """DMC method to create user"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str):
        """Create super user [admin]"""
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            # birthday = datetime.datetime.now()
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStamp):
    """main user model"""

    reporting_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    social_insurance_number = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    image = models.ImageField(upload_to="profile_image")
    email = models.EmailField(max_length=45, unique=True)
    mobile_number = models.CharField(max_length=15)
    telegram_link = models.CharField(max_length=100)
    birthday = models.DateField(null=True)
    team = models.CharField(max_length=20, choices=TEAM.choices)
    salary = models.JSONField(default=dict)
    location = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField(
        Skills,
        related_name="skills",
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE.choices)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = ChsrBaseUserManger()
    USERNAME_FIELD = "email"

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

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-first_name", "-last_name"]
        get_latest_by = "created_at"
