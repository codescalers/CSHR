"""This file contains everything related to the Event model."""
import datetime
from cshr.models.event import Event
from typing import List

from cshr.models.users import User


def get_event_by_id(id: str) -> Event:
    """Return event who have the same id"""
    try:
        return Event.objects.get(id=int(id))
    except Event.DoesNotExist:
        return None


def get_all_events() -> Event:
    """Return all events"""
    return Event.objects.all()


def filter_events_by_month_and_year(user: User, month: str, year: str) -> Event:
    """
    This function will filter all of events based on its yesr, month.
    """
    events: List[Event] = Event.objects.filter(
        from_date__month=month, from_date__year=year
    )
    return events


def filter_events_by_day(day: int) -> List[Event]:
    """Filter all users by birthdates"""
    today = datetime.datetime.now()
    return Event.objects.filter(
        from_date__year=today.year, from_date__month=today.month, from_date__day=day
    )
