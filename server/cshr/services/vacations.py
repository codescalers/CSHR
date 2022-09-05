"""This file contains everything related to the Vacation model."""
from server.cshr.models.vacations import Vacation
from django.db.models import Q
from typing import List


def filter_vacations_by_month_and_year(month: str, year: str) -> Vacation:
    """
    This function will filter all of vacations based on its yesr, month.
    """
    vacations: List[Vacation] = Vacation.objects.filter(
        Q(from_date__month=month, from_date__year=year)
        | Q(end_date__month=month, end_date__year=year)
    )
    return vacations

def get_vacation_by_id(id: str) -> Vacation:
    """Return vacation who have the same id"""
    try:
        return Vacation.objects.get(id=int(id))
    except Vacation.DoesNotExist:
        return None


def get_all_vacations() -> Vacation:
    """Return all hr letters"""
    return Vacation.objects.all()

