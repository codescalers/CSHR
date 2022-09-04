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
