from django.db import models

from server.cshr.models.abstracts import TimeStamp
from server.cshr.models.users import User


class EVALUATION_FORM_TYPE(models.TextChoices):
    PEER_2_PEER_FORM = "Peer 2 Peer Form"
    REVERSE_FORM = "Reverse Form"


class EVALUATION_QUARTER(models.TextChoices):
    JAN_MARCH = "1 : 3"
    APR_JUN = "4 : 6"
    JUL_SEP = "7 : 9"
    OCT_DEC = "10 : 12"


class Evaluations(TimeStamp):
    """Database model for evaluations"""

    form = models.CharField(max_length=50, choices=EVALUATION_FORM_TYPE.choices)
    quarter = models.CharField(max_length=150, choices=EVALUATION_FORM_TYPE.choices)
    link = models.CharField(max_length=150)

    def str(self) -> str:
        return f"({self.quarter}) - {self.created_at.year}"


class UserEvaluations(TimeStamp):
    """Database model for user evaluations"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quarter = models.CharField(max_length=150, choices=EVALUATION_FORM_TYPE.choices)
    link = models.CharField(max_length=150)
    score = models.IntegerField(default=0)

    def str(self) -> str:
        return self.user.full_name