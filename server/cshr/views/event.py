import datetime
from server.cshr.serializers.event import EventSerializer
from server.cshr.api.permission import UserIsAuthenticated
from server.cshr.services.event import get_all_events, get_event_by_id
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from server.cshr.api.response import CustomResponse
from server.cshr.utils.parse_date import CSHRDate


class EventApiView(ViewSet, GenericAPIView):
    """Class Event_APIVIEW to create a new event into database"""

    serializer_class = EventSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Method to create a new event"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            from_date: CSHRDate = CSHRDate(request.data.get("from_date"))
            from_date_parsing: datetime.datetime = from_date.parse() 
            end_date: CSHRDate = CSHRDate(request.data.get("end_date"))
            end_date_parsing: datetime.datetime = end_date.parse()
            if type(from_date_parsing) == datetime.datetime and  type(end_date_parsing) == datetime.datetime:
                serializer.save(date=from_date_parsing)
                return CustomResponse.success(
                    data=serializer.data,
                    message="event is created successfully",
                    status_code=201,
                )
            return from_date_parsing
        return CustomResponse.bad_request(
            error=serializer.errors, message="event creation failed"
        )

    def get_all(self, request: Request) -> Response:
        events = get_all_events()
        serializer = EventSerializer(events, many=True)
        return CustomResponse.success(
            data=serializer.data, message="events found", status_code=200
        )

    def get_one(self, request: Request, id: str, format=None) -> Response:
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
