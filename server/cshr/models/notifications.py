from django.db import models
from server.cshr.models.users import User
from server.cshr.models.abstracts import TimeStamp


""" database notification model """


class TYPE_CHOICES(models.TextChoices):
    """
    it is a list of choices for the notification type
    """

    HR_LETTERS = "hr_letters", "HR Letters"
    COMPENSATION = "compensation", "Compensation"
    VACATIONS = "vacations", "Vacations"
    EVENT = "event", "Event"


class Notifications(TimeStamp):
    creator_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator_user"
    )
    distination_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="distination_user"
    )
    body = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES.choices)

    def __str__(self) -> str:
        return self.host_user.first_name

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
