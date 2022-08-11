from django.db import models

from server.cshr.models.requests import Requests


class Compensation(Requests):
    """Class vacation model for adding a new vacation request to the database"""

    reason = models.CharField(max_length=250, blank=True)
    from_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
