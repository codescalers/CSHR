from ssl import CertificateError
from django.db import models

from server.cshr.models.abstracts import TimeStamp

from server.cshr.models.user import User


class Training_Courses(TimeStamp):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_courses"
    )
    name = models.CharField(max_length=45, null=False)
    certificate_link = models.CharField(max_length=150, null=False)