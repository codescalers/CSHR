from django.db import models
from server.cshr.models.abstracts import TimeStamp
from server.cshr.models.office import Office

from server.cshr.models.users import User

from server.cshr.models.requests import Requests
from django.core.exceptions import ValidationError


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
    taked_from_old_balance = models.BooleanField(default=False)

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
    public_holidays = models.IntegerField()
    date = models.DateField(auto_now=True)
    old_balance = models.JSONField(default=dict, null=True)
    actual_balance = models.JSONField(default=dict, null=True)

    def __str__(self):
        return str(self.user.email)

class PublicHoliday(TimeStamp):
    location = models.ForeignKey(Office, on_delete=models.CASCADE)
    holiday_date = models.DateField()

    class Meta:
        unique_together = ('holiday_date', 'location',)

    def __str__(self):
        return str(f"{self.location.country} - {self.holiday_date}")
