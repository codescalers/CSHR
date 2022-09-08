from django.db import models


from server.cshr.models.requests import Requests
from datetime import datetime

class HrLetters(Requests):
    """
    Class hr letters model for adding
    a new HR_letter request to the database
    """

    # who is sending to
    addresses = models.CharField(max_length=45)
    date = models.DateField(default=datetime.now)
    with_date= models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.addresses

    class Meta:
        verbose_name = "Hr Letter"
        verbose_name_plural = "Hr letters"
