from django.db import models

from server.cshr.models.abstracts import TimeStamp

from server.cshr.models.users import User


class Training_Courses(TimeStamp):
    """Class training_courses model for adding a new"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_courses"
    )
    name = models.CharField(max_length=45)
    certificate_link = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Training course"
        verbose_name_plural = "Training courses"
