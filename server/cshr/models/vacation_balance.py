from django.db import models
from server.cshr.models.users import User


class VacationBalance(models.Model):
    """User vacation balance model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    sick_leaves = models.IntegerField(default=5)
    compensation = models.IntegerField(default=0)
    unpaid = models.IntegerField(default=0)
    annual_leaves = models.IntegerField()
    emergencies = models.IntegerField(default=5)
    leave_execuses = models.IntegerField(default=4)
    public_holidays = models.IntegerField()
    date = models.DateField(auto_now=True)
    old_balance = models.JSONField(default=dict, null = True)
