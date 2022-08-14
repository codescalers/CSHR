"""abstract model for created, updated timestamps"""
from django.db import models


class TimeStamp(models.Model):
    """Database model for created and updated timestamps"""

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(db_index=True)

    class Meta:
        abstract = True
