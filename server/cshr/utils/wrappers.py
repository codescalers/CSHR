import datetime
from cshr.models.users import User
from cshr.models.vacations import Vacation, PublicHoliday
from cshr.models.meetings import Meetings
from cshr.models.event import Event
from cshr.serializers.event import EventSerializer
from cshr.serializers.public_holidays import PublicHolidaySerializer
from cshr.serializers.users import BaseUserSerializer
from cshr.serializers.vacations import LandingPageVacationsSerializer
from cshr.serializers.meetings import MeetingsSerializer
from enum import Enum

from cshr.services.users import build_user_reporting_to_hierarchy


class LandingPageTypeEnum(Enum):
    VACATION = "vacation"
    PUBLIC_HOLIDAY = "holiday"
    BIRTHDAY = "birthday"
    MEETING = "meeting"
    EVENT = "event"


def wrap_vacation_request(vacation: Vacation) -> LandingPageVacationsSerializer:  # type: ignore
    """
    Wrap the vacation request with [type: string] field, to be ready to be sent to the calendar as the `type` field is required there.
    """
    vacation_data = LandingPageVacationsSerializer(vacation).data
    vacation_data["type"] = LandingPageTypeEnum.VACATION.value
    vacation_data["applying_user_full_name"] = vacation.applying_user.full_name
    vacation_data["approvals"] = build_user_reporting_to_hierarchy(
        vacation.applying_user
    )
    return vacation_data


def wrap_meeting_request(meeting: Meetings) -> MeetingsSerializer:  # type: ignore
    """
    Wrap the meeting request with [type: string] field, to be ready to be sent to the calendar as the `type` field is required there.
    """
    meeting_data = MeetingsSerializer(meeting).data
    meeting_data["type"] = LandingPageTypeEnum.MEETING.value
    return meeting_data


def wrap_event_request(event: Event) -> EventSerializer:  # type: ignore
    """
    Wrap the event request with [type: string] field, to be ready to be sent to the calendar as the `type` field is required there.
    """
    event_data = EventSerializer(event).data
    event_data["type"] = LandingPageTypeEnum.EVENT.value
    return event_data


def wrap_holiday_request(holiday: PublicHoliday) -> PublicHolidaySerializer:  # type: ignore
    """
    Wrap the event request with [type: string] field, to be ready to be sent to the calendar as the `type` field is required there.
    """
    holiday_data = PublicHolidaySerializer(holiday).data
    holiday_data["type"] = LandingPageTypeEnum.PUBLIC_HOLIDAY.value
    return holiday_data


def wrap_birthday_event(birthday: User) -> BaseUserSerializer:  # type: ignore
    """
    Wrap the birthday request with [type: string] field, to be ready to be sent to the calendar as the `type` field is required there.
    """
    today = datetime.datetime.now()
    birthday_data = BaseUserSerializer(birthday).data
    birthday_data["type"] = LandingPageTypeEnum.BIRTHDAY.value
    birthday_data["date"] = (
        f"{today.year}-{birthday.birthday.month}-{birthday.birthday.day}"
    )
    return birthday_data
