from django.db import models
from cshr.models.abstracts import TimeStamp
from cshr.models.requests import Requests
from cshr.models.users import User


class DocumentsStatus(models.TextChoices):
    APPROVED = "approved", "Approved"
    UNDER_REVIEW = "Under-review", "under-review"
    REJECTED = "Rejected", "rejected"


class HrLetters(Requests):
    """
    Class hr letters model for adding
    a new HR_letter request to the database
    """

    # who is sending to
    addresses = models.CharField(max_length=45)
    with_salary_mentioned = models.BooleanField(default=False)
    with_date = models.BooleanField(default=False)
    from_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.addresses

    class Meta:
        verbose_name = "Hr Letter"
        verbose_name_plural = "Hr letters"


class UserDocuments(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=DocumentsStatus.choices,
        default=DocumentsStatus.UNDER_REVIEW,
    )

    def __str__(self) -> str:
        return self.user.email
