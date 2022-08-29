""" database office model """
from django.db import models

from server.cshr.models.abstracts import TimeStamp


class Office(TimeStamp):
    name = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    city = models.CharField(max_length=45)

    def __str__(self) -> str:
        return self.name

    class Meta:
        unique_together = ("name", "country", "city")
