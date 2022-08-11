from django.db import models

from server.cshr.models.abstracts import TimeStampedModel


from server.cshr.models.users import User
from server.cshr.models.vacations import Vacations
from server.cshr.models.hr_letters import Hr_letters
from server.cshr.models.compensations import Compensation


class TYPE_CHOICES(models.TextChoices):
    """
    it is a list of choices for the request type        
    """
    HR_LETTERS = "hr_letters", "HR Letters"
    COMPENSATION = "compensation", "Compensation"
    VACATIONS = "vacations", "Vacations"


class STATUS_CHOICES(models.TextChoices):
    """
    it is a list of choices for the request status
    """

    REJECTED = "rejected", "Rejected"
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"


class Requests(TimeStampedModel):
    """Class Requests model for adding a new
    Rwquest automatically  to the database"""

    # to use it User.user_requests.all()
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_requests"
    )
    # to use it User.user_vaccations.all()
    Vacations = models.ForeignKey(
        Vacations, on_delete=models.CASCADE, related_name="user_vacations"
    )
    Compensation = models.ForeignKey(
        Compensation, on_delete=models.CASCADE,
        related_name="user_compensation"
    )
    HR_LETTERS = models.ForeignKey(
        Hr_letters, on_delete=models.CASCADE, related_name="user_hr_letters"
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES.choices,
        default=TYPE_CHOICES.VACATION
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES.choices,
        default=STATUS_CHOICES.PENDING
    )
