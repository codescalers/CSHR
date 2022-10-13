import datetime
from typing import List
from server.cshr.serializers.meetings import MeetingsSerializer
from server.cshr.models.users import User
from server.cshr.api.permission import UserIsAuthenticated
from server.cshr.services.users import get_user_by_id
from server.cshr.services.meetings import get_all_meetings, get_meeting_by_id
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.api.response import CustomResponse

from server.cshr.utils.parse_date import CSHRDate


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
                serializer.save(
                    host_user=current_user, date=parsing, invited_users=invited_users
                )
                return CustomResponse.success(
                    data=serializer.data,
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
