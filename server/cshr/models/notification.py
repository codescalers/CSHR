from django.db import models

from cshr.models.abstracts import TimeStamp
from cshr.models.users import User
from cshr.models.requests import STATUS_CHOICES, Requests


class NotificationType(models.TextChoices):
    """types of notifications"""

    VACATION = "Vacation", "vacation"


class Notification(TimeStamp):
    """
    Database model for notifications with sender, receivers, title, body, and read status.

    Attributes:
        sender (User): The user who sent the notification.
        receivers (ManyToManyField): The users who received the notification.
        title (CharField): The title of the notification.
        body (TextField): The content/body of the notification.
        is_read (BooleanField): Indicates whether the notification has been read or not.
        request (NotificationType.choices): Indicates the object type of the notification e.g. vacation, hr_latter etc.

    Inherits:
        TimeStamp: Provides created_at and modified_at timestamps for the notification.

    Methods:
        __str__: Returns the email of the sender when the object is converted to a string.
    """

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_sender"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_receiver"
    )
    title = models.CharField(max_length=250)
    body = models.TextField()
    request = models.ForeignKey(
        Requests, on_delete=models.CASCADE, related_name="notification_request"
    )
    request_status = models.CharField(max_length=20, choices=STATUS_CHOICES.choices)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "request_status",
            "request",
            "receiver",
            "sender",
        )
