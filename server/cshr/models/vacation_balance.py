from django.db import models
from server.cshr.models.users import User


class VacationBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    sick_leaves = models.IntegerField(default=5)
    compensation = models.IntegerField(default=0)
    unpaid = models.IntegerField(default=0)
    annual_leaves = models.IntegerField()
    emergencies = models.IntegerField(default=5)
    leave_execuses = models.IntegerField(default=4)
    public_holidays = models.IntegerField()


class VacationBalanceValues(models.Model):
    sick_leaves = models.IntegerField(default=100)
    compensation = models.IntegerField(default=0)
    unpaid = models.IntegerField(default=0)
    annual_leaves = models.IntegerField(default=10)
    emergencies = models.IntegerField(default=5)
    leave_execuses = models.IntegerField(default=4)
    public_holidays = models.IntegerField(default=5)
