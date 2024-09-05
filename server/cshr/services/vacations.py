"""This file contains everything related to the Vacation model."""

from cshr.models.requests import STATUS_CHOICES, Requests
from cshr.models.users import User
from cshr.models.vacations import Vacation, VacationBalance
from django.db.models import Q
from django.db.models.query import QuerySet
from typing import List


def filter_vacations_by_month_and_year(month: str, year: str) -> Vacation:
    vacations: QuerySet[Vacation] = Vacation.objects.filter(
        Q(from_date__month=month, from_date__year=year) |
        Q(end_date__month=month, end_date__year=year)
    ).exclude(status__in=[STATUS_CHOICES.REJECTED, STATUS_CHOICES.CANCELED]).select_related('applying_user')
    return vacations


def get_vacation_by_id(id: str) -> Vacation:
    """Return vacation who have the same id"""
    try:
        return Vacation.objects.get(id=int(id))
    except Vacation.DoesNotExist:
        return None


def get_all_vacations() -> Vacation:
    """Return all vacations"""
    return Vacation.objects.all()


def filter_vacations_by_pending_status(team_lead_user: User) -> Vacation:
    """Return all vacations that has pending status"""
    users_reporting_to_teemlead_ids: List[int] = User.objects.filter(
        reporting_to=team_lead_user
    ).values_list("id", flat=True)
    return Vacation.objects.filter(
        status=STATUS_CHOICES.PENDING,
        applying_user__id__in=users_reporting_to_teemlead_ids,
    )


def get_vacations_by_user(id: str) -> Vacation:
    "Return all vacations for certain user"
    return Vacation.objects.filter(applying_user=id)


def get_balance_by_user(user: User) -> VacationBalance:
    try:
        return VacationBalance.objects.get(user=user)
    except VacationBalance.DoesNotExist:
        return None


def filter_balances_by_users(users: List[User]) -> VacationBalance:
    return VacationBalance.objects.filter(user__in=users)


def get_vacation_based_on_request(request_: Requests):
    """Returns vacation object who created at the sane time of request creation."""
    try:
        return Vacation.objects.get(
            # created_at__day = request_.created_at.day,
            applying_user__id=request_.applying_user.id,
            approval_user__id=request_.approval_user.id,
        )
    except Vacation.DoesNotExist:
        return None


def filter_user_vacations_by_pending_status(user: User) -> Vacation:
    """Return all vacations that has pending status and related to user"""
    return Vacation.objects.filter(
        status=STATUS_CHOICES.PENDING,
        applying_user=user,
    ).order_by("created_at")


def filter_user_vacations(user: User) -> Vacation:
    """Return all vacations that has pending status and related to user"""
    return Vacation.objects.filter(applying_user=user).order_by("created_at")
