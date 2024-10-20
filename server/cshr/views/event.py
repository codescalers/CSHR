from typing import Dict, List
from cshr.models.event import Event
from cshr.serializers.event import EventOnDaySerializer, EventSerializer
from cshr.api.permission import UserIsAuthenticated
from cshr.services.event import (
    filter_events_by_day,
    get_all_events,
    get_event_by_id,
)
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from cshr.api.response import CustomResponse
from cshr.utils.wrappers import wrap_event_request


class BaseEventsAPIView(ListAPIView, GenericAPIView):
    serializer_class = EventSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Method to create a new event"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            saved = serializer.save()
            response_date: Dict = wrap_event_request(saved)
            return CustomResponse.success(
                data=response_date,
                message="event is created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="event creation failed"
        )

    def get_queryset(self) -> Response:
        return get_all_events().order_by("-created_at")


class EventApiView(GenericAPIView):
    """Class Event_APIVIEW to create a new event into database"""

    serializer_class = EventSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, id: str, format=None) -> Response:
        """method to get a single event by id"""
        event = get_event_by_id(id=id)
        if event is None:
            return CustomResponse.not_found(
                message="event is not found", status_code=404
            )

        serializer = EventSerializer(event)
        return CustomResponse.success(
            data=serializer.data, message="event found", status_code=200
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete an event by id"""
        event = get_event_by_id(id=id)
        if event is not None:
            event.delete()
            return CustomResponse.success(message="event deleted", status_code=204)
        return CustomResponse.not_found(message="event not found", status_code=404)

    def put(self, request: Request, id: str, format=None) -> Response:
        event = get_event_by_id(id=id)
        if event is None:
            return CustomResponse.not_found(message="event not found")
        serializer = self.get_serializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="event updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="event failed to update"
        )


class GetEventOnDayAPIView(GenericAPIView):
    """Class to filter all event based on requested day."""

    serializer_class = EventOnDaySerializer
    permission_classes = [
        UserIsAuthenticated,
    ]

    def get(self, request: Request) -> Response:
        """Get all meetings based on requested day that sent as a query param"""
        if not request.query_params.get("day"):
            return CustomResponse.bad_request(
                message="You must send the day to filter based on it."
            )
        day: int = int(request.query_params.get("day"))
        events: List[Event] = filter_events_by_day(day)
        serializer = self.serializer_class(events, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Events founded successfully."
        )
