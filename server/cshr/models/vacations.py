from django.db import models

from server.cshr.models.users import User

from server.cshr.models.requests import Requests


class REASON_CHOICES(models.TextChoices):
    """
    enum for the vacation Reason
    """

    ANNUAL_LEAVES = "annual_leaves", "Annual Leaves"
    PUBLIC_HOLIDAYS = "public_holidays", "Public Holidays"
    EMERGENCY_LEAVE = "emergency_leave", "Emergency Leave"
    LEAVE_EXCUSES = "leave_excuses", "Leave Excuses"


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

    @property
    def __name__(self):
        return "vacations"


class PublicHolidays(models.Model):
    date = models.DateField()


class VacationBalance(models.Model):
    """User vacation balance model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    sick_leaves = models.IntegerField()
    compensation = models.IntegerField()
    unpaid = models.IntegerField()
    annual_leaves = models.IntegerField()
    emergencies = models.IntegerField()
    leave_execuses = models.IntegerField()
    public_holidays = models.ManyToManyField(PublicHolidays)
    date = models.DateField(auto_now=True)
    old_balance = models.JSONField(default=dict, null=True)
