from django.db import models
from server.cshr.models.abstracts import TimeStamp
from server.cshr.models.requests import Requests
from server.cshr.models.users import User


class DocementsStatus(models.TextChoices):
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
    date = models.DateField(auto_now=True)
    with_date = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.addresses

    class Meta:
        verbose_name = "Hr Letter"
        verbose_name_plural = "Hr letters"


class UserDocements(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=DocementsStatus.choices,
        default=DocementsStatus.UNDER_REVIEW,
    )

    def __str__(self) -> str:
        return self.user.email
