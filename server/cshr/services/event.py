"""This file contains everything related to the Event model."""
import datetime
from server.cshr.models.event import Event
from typing import Any, Dict, List

from server.cshr.models.users import User
from server.cshr.serializers.event import EventSerializer


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


def send_event_to_calendar(event: Event) -> Dict[str, Any]:
    from server.cshr.services.landing_page import (
        LandingPageClassNameEnum,
        LandingPageTypeEnum,
    )

    """
    Takes the standerd event, then update it with calendar values.
        calendar pattern:
            - {
                "title": str(event),
                "date": date(from_date),
                "len": int(len(end_date - from_date)),
                "className": str(--task-warning),
                "eventName": str(event)
            }
    """
    response: Dict(str, Any) = {}
    response["len"] = (event.end_date - event.from_date).days + 1
    response["date"] = event.from_date
    response["title"] = LandingPageTypeEnum.Event.value
    response["className"] = LandingPageClassNameEnum.Event.value
    response["isBottom"] = True
    response["eventName"] = LandingPageTypeEnum.Event.value
    response["event"] = [EventSerializer(event).data]
    return response
