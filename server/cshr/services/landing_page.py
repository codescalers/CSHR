"""This file contains everything related to the landing page functionalty."""
from cshr.models.users import User
from cshr.serializers.event import EventSerializer
from cshr.serializers.meetings import MeetingsSerializer
from cshr.serializers.public_holidays import PublicHolidaySerializer
from cshr.serializers.users import BaseUserSerializer
from cshr.serializers.vacations import LandingPageVacationsSerializer
from cshr.services.event import filter_events_by_month_and_year
from cshr.services.meetings import filter_meetings_by_month_and_year
from cshr.services.public_holidays import (
    filter_public_holidays_by_month_and_year,
)
from cshr.services.users import filter_users_by_birth_month
from cshr.services.vacations import filter_vacations_by_month_and_year
from typing import Any, List
from enum import Enum
import datetime


class LandingPageTypeEnum(Enum):
    VACATION = "vacation"
    PUBLIC_HOLIDAY = "holiday"
    BIRTHDAY = "birthday"
    MEETING = "meeting"
    EVENT = "event"

def landing_page_calendar_functionality(user: User, month: str, year: str) -> List[Any]:
    response: List[Any] = []

    # Fetch vacations
    vacations = filter_vacations_by_month_and_year(month, year).order_by("-created_at")
    for vacation in vacations:
        vacation_data = LandingPageVacationsSerializer(vacation).data
        vacation_data["type"] = LandingPageTypeEnum.VACATION.value
        vacation_data["applying_user_full_name"] = vacation.applying_user.full_name
        response.append(vacation_data)

    # Fetch meetings
    meetings = filter_meetings_by_month_and_year(user, month, year).order_by("-created_at")
    for meeting in meetings:
        meeting_data = MeetingsSerializer(meeting).data
        meeting_data["type"] = LandingPageTypeEnum.MEETING.value
        response.append(meeting_data)

    # Fetch events
    events = filter_events_by_month_and_year(user, month, year).order_by("-created_at")
    for event in events:
        event_data = EventSerializer(event).data
        event_data["type"] = LandingPageTypeEnum.EVENT.value
        response.append(event_data)

    # Fetch users' birthdays
    users_birthdates = filter_users_by_birth_month(month).order_by("-created_at")
    for birthday_user in users_birthdates:
        today = datetime.datetime.now()
        birthday_data = BaseUserSerializer(birthday_user).data
        birthday_data["type"] = LandingPageTypeEnum.BIRTHDAY.value
        birthday_data["date"] = f"{today.year}-{birthday_user.birthday.month}-{birthday_user.birthday.day}"
        response.append(birthday_data)

    # Fetch public holidays
    public_holidays = filter_public_holidays_by_month_and_year(year, month).order_by("-created_at")
    for holiday in public_holidays:
        holiday_data = PublicHolidaySerializer(holiday).data
        holiday_data["type"] = LandingPageTypeEnum.PUBLIC_HOLIDAY.value
        response.append(holiday_data)

    return response
