from django.db import models


from server.cshr.models.requests import Requests


class HrLetters(Requests):
    """
    Class vacation model for adding
    a new HR_letter request to the database
    """

    # who is sending to
    addresses = models.CharField(max_length=45)

    def __str__(self) -> str:
        return self.addresses

    class Meta:
        verbose_name = "Hr Letter"
        verbose_name_plural = "Hr letters"
