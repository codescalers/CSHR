"""This file contains everything related to the landing page functionalty."""
from server.cshr.models.event import Event
from server.cshr.models.meetings import Meetings
from server.cshr.models.users import User
from server.cshr.models.vacations import Vacation
from server.cshr.models.requests import TYPE_CHOICES
from server.cshr.serializers.event import EventSerializer
from server.cshr.serializers.meetings import MeetingsSerializer
from server.cshr.serializers.users import BaseUserSerializer
from server.cshr.serializers.vacations import LandingPageVacationsSerializer
from server.cshr.services.event import filter_events_by_month_and_year
from server.cshr.services.meetings import filter_meetings_by_month_and_year
from server.cshr.services.users import filter_users_by_berithday_month
from server.cshr.services.vacations import filter_vacations_by_month_and_year
from typing import Any, List, Dict, Union
from itertools import chain


def landing_page_calendar_functionality(user: User, month: str, year: str):
    """
    This function will filter all of events based on its yesr, month.
    """
    vacations: List[Vacation] = filter_vacations_by_month_and_year(month, year)
    meetings: List[Meetings] = filter_meetings_by_month_and_year(user, month, year)
    events: List[Event] = filter_events_by_month_and_year(user, month, year)
    users_birthdates: List[User] = filter_users_by_berithday_month(month)

    objects: Union[List[Any], None] = list(
        chain(vacations, events, meetings, users_birthdates)
    )
    response: Dict = {}

    for obj in objects:
        if hasattr(obj, "birthday"):
            # Thats mean user table
            response[obj.birthday.day] = {}
        elif hasattr(obj, "meeting_link") and not response.get(obj.date.day):
            # Thats mean meetings.
            response[obj.date.day] = {}
        elif hasattr(obj, "people") and not response.get(obj.from_date.day):
            # Thats mean events.
            response[obj.from_date.day] = {}
        elif hasattr(obj, "type") and obj.type == TYPE_CHOICES.VACATIONS:
            # vacations
            response[obj.from_date.day] = {}
        else:
            continue

    for obj, _ in response.items():
        for user in users_birthdates:
            # birthdates
            if user.birthday.day == obj:
                response[obj]["birthdates"] = BaseUserSerializer(
                    users_birthdates.filter(birthday__day=obj), many=True
                ).data

        for vacation in vacations:
            # vacations
            if vacation.from_date.day == obj:
                response[obj]["vacations"] = LandingPageVacationsSerializer(
                    vacations.filter(from_date__day=vacation.from_date.day), many=True
                ).data
            elif vacation.end_date.day == obj:
                response[obj]["vacations"] = LandingPageVacationsSerializer(
                    vacations.filter(end_date__day=vacation.end_date.day), many=True
                ).data

        for meeting in meetings:
            # meetings
            if meeting.date.day == obj:
                response[obj]["meetings"] = MeetingsSerializer(meetings, many=True).data

        for event in events:
            # events
            if event.from_date.day == obj:
                response[obj]["events"] = EventSerializer(
                    events.filter(from_date__day=event.from_date.day), many=True
                ).data

            if event.end_date.day == obj:
                response[obj]["events"] = EventSerializer(
                    events.filter(end_date__day=event.end_date.day), many=True
                ).data
    return response
