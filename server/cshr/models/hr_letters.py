from django.db import models


from server.cshr.models.requests import Requests


class HR_LETTERS(Requests):
    """Class vacation model for adding a new HR_letter request to the database"""
    addresses = models.CharField(max_length=45, null=False)
