from django.db import models


from server.cshr.models.requests import Requests


class HrLetters(Requests):
    """
    Class hr letters model for adding
    a new HR_letter request to the database
    """

    addresses = models.CharField(max_length=45)

    def __str__(self) -> str:
        return self.addresses

    class Meta:
        verbose_name = "Hr Letter"
        verbose_name_plural = "Hr letters"
