from django.db import models
from server.cshr.models.users import User
from server.cshr.models.abstracts import TimeStamp


""" database event model """


class Event(TimeStamp):

    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    people = models.ManyToManyField(User, related_name="event_participants")
    location = models.TextField(max_length=300)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
