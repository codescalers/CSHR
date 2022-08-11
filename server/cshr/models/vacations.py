from django.db import models

from server.cshr.models.requests import Requests


class REASON_CHOICES(models.TextChoices):
    """
    enum for the vacation Reason
    """
    ANNUAL_LEAVES = "annual_leaves", "Annual Leaves"
    PUBLIC_HOLIDAYS = "public_holidays", "Public Holidays"
    EMERGENCY_LEAVE = "emergency_leave", "Emergency Leave"
    LEAVE_EXCUSES = "emergency_leave", "Leave Excuses"


class Vacation(Requests):
    """Class vacation model for adding a new vacation request to the database"""
    reason = models.CharField(
        max_length=20, choices=REASON_CHOICES.choices, default=REASON_CHOICES.VACATION
    )
    from_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    change_log = models.JSONField(default=list)

    def ___str__(self):
        return self.reason
