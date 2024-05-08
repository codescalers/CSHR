"""This file contains everything related to the Meetings model."""
from cshr.models.meetings import Meetings
from typing import List

from cshr.models.users import User


def get_meeting_by_id(id: str) -> Meetings:
    """Return meeting who have the same id"""
    try:
        return Meetings.objects.get(id=int(id))
    except Meetings.DoesNotExist:
        return None


def get_all_meetings() -> Meetings:
    """Return all meetings"""
    return Meetings.objects.all()


def filter_meetings_by_month_and_year(user: User, month: str, year: str) -> Meetings:
    """
    This function will filter all of meetings based on its yesr, month.
    """
    meetings: List[Meetings] = Meetings.objects.filter(
        date__month=month, date__year=year
    )
    return meetings


def filter_meetings_by_day(year: int, month: int, day: int) -> List[Meetings]:
    """Filter all users by birthdates"""
    return Meetings.objects.filter(date__year=year, date__month=month, date__day=day)
