""" database office model """
from django.db import models

from cshr.models.abstracts import TimeStamp


class WEEKEND_DAYS(models.TextChoices):
    """Weekenh holidays choices"""

    Friday_and_Saturday = "Friday:Saturday", "Friday:Saturday"
    Saturday_and_Sunday = "Saturday:Sunday", "Saturday:Sunday"


class Office(TimeStamp):
    name = models.CharField(max_length=45, unique=True)
    country = models.CharField(max_length=45)
    weekend = models.CharField(
        max_length=20,
        choices=WEEKEND_DAYS.choices,
        default=WEEKEND_DAYS.Friday_and_Saturday,
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        unique_together = (
            "name",
            "country",
        )
