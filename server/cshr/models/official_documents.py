from django.db import models
from cshr.models.requests import Requests


class OffcialDocument(Requests):
    document = models.TextField()

    def __str__(self) -> str:
        return self.applying_user.email
