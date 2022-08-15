""" database user model """

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from server.cshr.models.abstracts import TimeStamp
from server.cshr.models.office import Office
from server.cshr.models.skills import Skills

class TestTrackerBaseUserManger(BaseUserManager):
    """This is the main class for user manger"""
    def create_user(self, email: str, password: str) -> 'User':
        """DMC method to create user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_admin(self, email: str, password: str):
        """ Create super user [admin] """
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
        )
        user.user_type = USER_TYPE.ADMIN
        user.save(using=self._db)
        return user
    def create_supervisor(self, email: str, password: str):
        """ Create super user [admin] """
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
        )
        user.user_type = USER_TYPE.SUPERVISOR
        user.save(using=self._db)
        return user






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
    image = models.ImageField(default='DEFAULT VALUE')
    email = models.EmailField(max_length=45, unique = True)
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
    objects = TestTrackerBaseUserManger()
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['first_name','last_name','telegram_link','birthday', 'mobile_number'] 
    @property
    def full_name(self) -> str:
        "return the user's full name"
        return '%s %s' % (self.first_name.title(), self.last_name.title())

    def __str__(self) -> str:
        return f"{self.email}"
