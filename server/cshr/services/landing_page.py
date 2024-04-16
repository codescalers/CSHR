"""This file contains everything related to the landing page functionalty."""

from cshr.models.users import User
from cshr.services.event import filter_events_by_month_and_year
from cshr.services.meetings import filter_meetings_by_month_and_year
from cshr.services.public_holidays import (
    filter_public_holidays_by_month_and_year,
)
from cshr.services.users import filter_users_by_birth_month
from cshr.services.vacations import filter_vacations_by_month_and_year
from typing import Any, List

from cshr.utils.wrappers import (
    wrap_birthday_event,
    wrap_event_request,
    wrap_holiday_request,
    wrap_meeting_request,
    wrap_vacation_request,
)


def landing_page_calendar_functionality(user: User, month: str, year: str) -> List[Any]:
    response: List[Any] = []

    # Fetch vacations
    vacations = filter_vacations_by_month_and_year(month, year).order_by("-created_at")
    for vacation in vacations:
        vacation_data = wrap_vacation_request(vacation)
        response.append(vacation_data)

    # Fetch meetings
    meetings = filter_meetings_by_month_and_year(user, month, year).order_by(
        "-created_at"
    )
    for meeting in meetings:
        meeting_data = wrap_meeting_request(meeting)
        response.append(meeting_data)

    # Fetch events
    events = filter_events_by_month_and_year(user, month, year).order_by("-created_at")
    for event in events:
        event_data = wrap_event_request(event)
        response.append(event_data)

    # Fetch users' birthdays
    users_birthdates = filter_users_by_birth_month(month).order_by("-created_at")
    for birthday_user in users_birthdates:
        birthday_data = wrap_birthday_event(birthday_user)
        response.append(birthday_data)

    # Fetch public holidays
    public_holidays = filter_public_holidays_by_month_and_year(year, month).order_by(
        "-created_at"
    )
    for holiday in public_holidays:
        holiday_data = wrap_holiday_request(holiday)
        response.append(holiday_data)

    return response
