"""This file contains everything related to the Meetings model."""
from server.cshr.models.meetings import Meetings
from typing import Any, Dict, List

from server.cshr.models.users import User
from server.cshr.serializers.meetings import MeetingsSerializer


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


def send_meeting_to_calendar(meeting: Meetings) -> Dict[str, Any]:
    from server.cshr.services.landing_page import (
        LandingPageClassNameEnum,
        LandingPageTypeEnum,
    )

    """
    Takes the standerd meeting, then update it with calendar values.
        calendar pattern:
            - {
                "title": str(meeting),
                "date": date(from_date),
                "len": int(len(end_date - from_date)),
                "className": str(--task-warning),
                "eventName": str(meeting)
            }
    """
    response: Dict(str, Any) = {}
    response["title"] = LandingPageTypeEnum.MEETING.value
    response["className"] = LandingPageClassNameEnum.MEETING.value
    response["eventName"] = LandingPageTypeEnum.MEETING.value
    response["meeting"] = [MeetingsSerializer(meeting).data]
    response["len"] = 1
    response["date"] = meeting.date
    return response
