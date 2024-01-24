from django.db import models
from cshr.models.users import User
from cshr.models.abstracts import TimeStamp


""" database meeting model """


class Meetings(TimeStamp):
    host_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="host_user"
    )
    invited_users = models.ManyToManyField(User, related_name="invited_users")
    location = models.CharField(max_length=250, default="remote")
    meeting_link = models.CharField(max_length=250)
    date = models.DateTimeField()

    def __str__(self) -> str:
        return self.host_user.email

    class Meta:
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"
