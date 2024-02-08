from django.db import models
from cshr.models.abstracts import TimeStamp
from cshr.models.office import Office

from cshr.models.users import User

from cshr.models.requests import Requests
import datetime


class REASON_CHOICES(models.TextChoices):
    """
    enum for the vacation Reason
    """

    PUBLIC_HOLIDAYS = "public_holidays", "Public Holidays"
    EMERGENCY_LEAVE = "emergency_leaves", "Emergency Leave"
    ANNUAL_LEAVES = "annual_leaves", "Annual Leaves"
    LEAVE_EXCUSES = "leave_excuses", "Leave Excuses"
    SICK_LEAVES = "sick_leaves", "Sick Leave"
    UNPAID = "unpaid", "unpaid"
    COMPENSATION = "compensation", "compensation"


class Vacation(Requests):
    """
    Class vacation model for adding
    a new vacation request to the database
    """

    reason = models.CharField(
        max_length=20,
        choices=REASON_CHOICES.choices,
        default=REASON_CHOICES.ANNUAL_LEAVES,
    )
    from_date = models.DateField()
    end_date = models.DateField()
    change_log = models.JSONField(default=list)

    def ___str__(self):
        return self.reason


class VacationBalance(models.Model):
    """User vacation balance model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    sick_leaves = models.IntegerField()
    compensation = models.IntegerField()
    unpaid = models.IntegerField()
    annual_leaves = models.IntegerField()
    emergency_leaves = models.IntegerField()
    leave_excuses = models.IntegerField()
    office_vacation_balance = models.ForeignKey("OfficeVacationBalance", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.user.email)


class PublicHoliday(TimeStamp):
    location = models.ForeignKey(Office, on_delete=models.CASCADE)
    holiday_date = models.DateField()
    expired = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "holiday_date",
            "location",
        )

    def __str__(self):
        return str(f"{self.location.country} - {self.holiday_date}")


class OfficeVacationBalance(TimeStamp):
    location = models.ForeignKey(Office, on_delete=models.CASCADE)
    year = models.IntegerField(default=datetime.datetime.now().year)
    annual_leaves = models.IntegerField(default=20)
    sick_leaves = models.IntegerField(default=365)
    compensation = models.IntegerField(default=365)
    unpaid = models.IntegerField(default=365)
    leave_excuses = models.IntegerField(default=6)
    emergency_leaves = models.IntegerField(default=6)
    public_holidays = models.ManyToManyField(
        "PublicHoliday", related_name="public_holidays"
    )

    class Meta:
        unique_together = (
            "year",
            "location",
        )

    def __str__(self):
        return str(f"{self.location.country} - {self.year}")
