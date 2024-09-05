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

from concurrent.futures import ThreadPoolExecutor


def landing_page_calendar_functionality(user: User, month: str, year: str) -> List[Any]:
    response: List[Any] = []

    with ThreadPoolExecutor() as executor:
        future_vacations = executor.submit(filter_vacations_by_month_and_year, month, year)
        future_meetings = executor.submit(filter_meetings_by_month_and_year, user, month, year)
        future_events = executor.submit(filter_events_by_month_and_year, user, month, year)
        future_birthdays = executor.submit(filter_users_by_birth_month, month)
        future_holidays = executor.submit(filter_public_holidays_by_month_and_year, year, month)

        # Add vacations to response
        for vacation in future_vacations.result():
            vacation_data = wrap_vacation_request(vacation)
            response.append(vacation_data)

        # Add meetings to response
        for meeting in future_meetings.result():
            meeting_data = wrap_meeting_request(meeting)
            response.append(meeting_data)

        # Add events to response
        for event in future_events.result():
            event_data = wrap_event_request(event)
            response.append(event_data)

        # Add birthdays to response
        for birthday_user in future_birthdays.result():
            birthday_data = wrap_birthday_event(birthday_user)
            response.append(birthday_data)

        # Add public holidays to response
        for holiday in future_holidays.result():
            holiday_data = wrap_holiday_request(holiday)
            response.append(holiday_data)

    return response