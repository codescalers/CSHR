import datetime
from typing import Dict, List
from cshr.serializers.meetings import MeetingsSerializer
from cshr.models.users import User
from cshr.api.permission import UserIsAuthenticated
from cshr.services.users import get_user_by_id
from cshr.services.meetings import (
    filter_meetings_by_day,
    get_all_meetings,
    get_meeting_by_id,
    send_meeting_to_calendar,
)
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from cshr.api.response import CustomResponse

from cshr.utils.parse_date import CSHRDate


class BaseMeetingsApiView(ListAPIView, GenericAPIView):
    """Class Meeting_APIVIEW to create a new meeting into database"""

    serializer_class = MeetingsSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Method to create a new meeting"""
        serializer = self.get_serializer(data=request.data)
        invited_users: List[int] = request.data.get("invited_users")
        if serializer.is_valid():
            current_user: User = get_user_by_id(request.user.id)
            provided_date: CSHRDate = CSHRDate(request.data.get("date"))
            parsing: datetime.datetime = provided_date.parse()
            if type(parsing) == datetime.datetime:
                saved = serializer.save(
                    host_user=current_user, date=parsing, invited_users=invited_users
                )
                response_date: Dict = send_meeting_to_calendar(saved)
                return CustomResponse.success(
                    data=response_date,
                    message="meeting is created successfully",
                    status_code=201,
                )
            return parsing
        return CustomResponse.bad_request(
            error=serializer.errors, message="meeting creation failed"
        )

    def get_queryset(self) -> Response:
        query_set = get_all_meetings()
        return query_set


class MeetingsApiView(ListAPIView, GenericAPIView):
    serializer_class = MeetingsSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, id: str, format=None) -> Response:
        """method to get a single meeting by id"""
        meeting = get_meeting_by_id(id=id)
        if meeting is None:
            return CustomResponse.not_found(
                message="meeting is not found", status_code=404
            )

        serializer = MeetingsSerializer(meeting)
        if meeting is not None:
            return CustomResponse.success(
                data=serializer.data, message="meeting found", status_code=200
            )
        return CustomResponse.not_found(message="meeting not found", status_code=404)

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete a meeting by id"""
        meeting = get_meeting_by_id(id=id)
        if meeting is not None:
            meeting.delete()
            return CustomResponse.success(message="meeting deleted", status_code=204)
        return CustomResponse.not_found(message="meeting not found", status_code=404)

    def put(self, request: Request, id: str) -> Response:
        meeting = get_meeting_by_id(id=id)
        if meeting is None:
            return CustomResponse.not_found(message="meeting not found")
        serializer = self.get_serializer(meeting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="meeting updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="meeting failed to update"
        )


class GetMeetingsOnDayAPIView(GenericAPIView):
    """Class to filter all meetings based on requested day."""

    serializer_class = MeetingsSerializer
    permission_classes = [
        UserIsAuthenticated,
    ]

    def get(self, request: Request) -> Response:
        """Get all meetings based on requested day that sent as a query param"""
        if (
            not request.query_params.get("day")
            or not request.query_params.get("month")
            or not request.query_params.get("year")
        ):
            return CustomResponse.bad_request(
                message="You must send [year, month, day] to filter based on it."
            )
        year: int = int(request.query_params.get("year"))
        month: int = int(request.query_params.get("month"))
        day: int = int(request.query_params.get("day"))
        events: List[User] = filter_meetings_by_day(year, month, day)
        serializer = self.serializer_class(events, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Meetings founded successfully."
        )
