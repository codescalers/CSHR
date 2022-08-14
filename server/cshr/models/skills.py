""" database office model """
from django.db import models


class Skills(models.Model):
    Name = models.CharField(max_length=50)
