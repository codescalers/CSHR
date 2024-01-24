"""This file contains everything related to the landing page functionalty."""
import datetime
from cshr.api.response import CustomResponse
from cshr.models.event import Event
from cshr.models.meetings import Meetings
from cshr.models.users import User
from cshr.models.vacations import PublicHoliday, Vacation
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
from cshr.services.users import filter_users_by_berithday_month
from cshr.services.vacations import filter_vacations_by_month_and_year
from typing import Any, List, Dict, Union
from itertools import chain
from enum import Enum


class LandingPageTypeEnum(Enum):
    VACATION = "vacation"
    PUBLIC_HOLIDAY = "public_holiday"
    BIRTHDAY = "birthday"
    MEETING = "meeting"
    Event = "event"


class LandingPageClassNameEnum(Enum):
    PUBLIC_HOLIDAY = "task--success"
    VACATION = "task--warning"
    BIRTHDAY = "task--primary"
    MEETING = "task--danger"
    Event = "task--info"


def landing_page_calendar_functionality(user: User, month: str, year: str):
    """
    This function will filter all of events based on its yesr, month.
    """
    vacations: List[Vacation] = filter_vacations_by_month_and_year(
        month, year
    ).order_by("-created_at")
    meetings: List[Meetings] = filter_meetings_by_month_and_year(
        user, month, year
    ).order_by("-created_at")
    events: List[Event] = filter_events_by_month_and_year(user, month, year).order_by(
        "-created_at"
    )
    users_birthdates: List[User] = filter_users_by_berithday_month(month).order_by(
        "-created_at"
    )
    public_holidays: PublicHoliday = filter_public_holidays_by_month_and_year(
        year, month
    ).order_by("-created_at")

    objects: Union[List[Any], None] = list(
        chain(public_holidays, vacations, events, meetings, users_birthdates)
    )

    response: List[Any] = []

    for object in objects:
        obj: Dict = {}
        obj["id"] = object.id
        if isinstance(object, Vacation):
            obj["title"] = LandingPageTypeEnum.VACATION.value
            obj["className"] = LandingPageClassNameEnum.VACATION.value
            obj["eventName"] = LandingPageTypeEnum.VACATION.value
            obj["vacation"] = LandingPageVacationsSerializer(
                vacations.filter(
                    from_date__day=object.from_date.day,
                    from_date__month=object.from_date.month,
                ),
                many=True,
            ).data
        elif isinstance(object, PublicHoliday):
            obj["title"] = LandingPageTypeEnum.PUBLIC_HOLIDAY.value
            obj["className"] = LandingPageClassNameEnum.PUBLIC_HOLIDAY.value
            obj["eventName"] = LandingPageTypeEnum.PUBLIC_HOLIDAY.value
            obj["holidays"] = PublicHolidaySerializer(
                public_holidays.filter(
                    holiday_date__day=object.holiday_date.day,
                    holiday_date__month=object.holiday_date.month,
                ),
                many=True,
            ).data
            obj["date"] = object.holiday_date
            obj["len"] = 1
        elif isinstance(object, Meetings):
            obj["title"] = LandingPageTypeEnum.MEETING.value
            obj["date"] = object.date
            obj["len"] = 1
            obj["vlen"] = 2
            obj["className"] = LandingPageClassNameEnum.MEETING.value
            obj["eventName"] = LandingPageTypeEnum.MEETING.value
            obj["meeting"] = MeetingsSerializer(
                meetings.filter(
                    date__day=object.date.day, date__month=object.date.month
                ),
                many=True,
            ).data
        elif isinstance(object, Event):
            obj["len"] = (object.end_date - object.from_date).days + 1
            obj["date"] = object.from_date
            obj["title"] = LandingPageTypeEnum.Event.value
            obj["className"] = LandingPageClassNameEnum.Event.value
            obj["isBottom"] = True
            obj["eventName"] = LandingPageTypeEnum.Event.value
            obj["event"] = EventSerializer(
                events.filter(
                    from_date__day=object.from_date.day,
                    from_date__month=object.from_date.month,
                    from_date__year=object.from_date.year,
                ),
                many=True,
            ).data
        elif isinstance(object, User):
            today = datetime.datetime.now()
            obj["title"] = LandingPageTypeEnum.BIRTHDAY.value
            obj["className"] = LandingPageClassNameEnum.BIRTHDAY.value
            obj["eventName"] = LandingPageTypeEnum.BIRTHDAY.value
            obj["date"] = f"{today.year}-{object.birthday.month}-{object.birthday.day}"
            obj["len"] = 1
            obj["vlen"] = 2
            obj["users"] = BaseUserSerializer(
                users_birthdates.filter(
                    birthday__day=object.birthday.day,
                    birthday__month=object.birthday.month,
                ),
                many=True,
            ).data
        else:
            return CustomResponse.bad_request(message="Unknown landing page type")

        if (
            hasattr(object, "from_date")
            and hasattr(object, "end_date")
            and not isinstance(object, Event)
        ):
            obj["len"] = (object.end_date - object.from_date).days + 1
            obj["date"] = object.from_date
        response.append(obj)

    return response
