from django.db import models
from server.cshr.models.abstracts import TimeStamp
from server.cshr.models.requests import STATUS_CHOICES, TYPE_CHOICES
from server.cshr.models.users import User


class OffcialDocument(TimeStamp):
    applying_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="official_document_applying_user"
    )
    approval_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="official_document_approval_user",
        null=True,
        blank=True,
    )
    document = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES.choices)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES.choices,
        default=TYPE_CHOICES.OFFICIAL_DOCUMENT,
    )

    def __str__(self) -> str:
        return self.applying_user.email
