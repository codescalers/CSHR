from django.db import models

from server.cshr.models.abstracts import TimeStamp
from server.cshr.models.users import User


class Evaluations(TimeStamp):
    """Database model for evaluations"""

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    link = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"user id :{self.user} {self.link}"
