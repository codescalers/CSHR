""" database office model """
from email.policy import default
from django.db import models

from server.cshr.models.abstracts import TimeStamp

class WEEKEND_DAYS(models.TextChoices):
    """Weekenh holidays choices"""
    Friday_and_Saturday     = "Friday:Saturday", "Friday:Saturday"
    Saturday_and_Sunday     = "Saturday:Sunday", "Saturday:Sunday"
    Sunday_and_Monday       = "Sunday:Monday", "Sunday:Monday"
    Monday_and_Tuesday      = "Monday:Tuesday", "Monday:Tuesday"
    Tuesday_and_Wednesday   = "Tuesday:Wednesday", "Tuesday:Wednesday"
    Wednesday_and_Thursday  = "Wednesday:Thursday", "Wednesday:Thursday"
    Thursday_and_Friday     = "Thursday:Friday", "Thursday:Friday"

class Office(TimeStamp):
    name = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    weekend = models.CharField(
        max_length=20,
        choices=WEEKEND_DAYS.choices,
        default=WEEKEND_DAYS.Friday_and_Saturday
    )

    def __str__(self) -> str:
        return f"{self.name}"
