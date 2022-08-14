from django.db import models
from server.cshr.models.users import User


class Company_properties(models.Model):
    name = models.CharField(max_length=45)
    image_of = models.CharField(max_length=140, null=True, blank=True)
    user = models.ForeignKey(User,  on_delete=models.DO_NOTHING)
