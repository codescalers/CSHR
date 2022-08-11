""" database office model """
from django.db import models

from server.cshr.models.abstracts import TimeStamp


class Office(TimeStamp):
    name = models.CharField(max_length=45)
    country = models.CharField(max_length=45)