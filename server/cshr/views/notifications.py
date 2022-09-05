from server.cshr.serializers.notifications import NotificationSerializer
from server.cshr.models.users import User
from server.cshr.api.permission import UserIsAuthenticated
from server.cshr.services.users import get_user_by_id
from server.cshr.services.notifications import (
    get_all_notiifications,
    get_notification_by_id,
)
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from server.cshr.api.response import CustomResponse


class NotificationApiView(ViewSet, GenericAPIView):
    """Class Notification_APIVIEW to create a new meeting into database"""

    serializer_class = NotificationSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Method to create a new notification"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            currentUser: User = get_user_by_id(request.user.id)
            serializer.save(creator_user=currentUser)
            return CustomResponse.success(
                data=serializer.data,
                message="notification is created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="notification creation failed"
        )

    def get_all(self, request: Request) -> Response:
        notiifications = get_all_notiifications()
        serializer = NotificationSerializer(notiifications, many=True)
        return CustomResponse.success(
            data=serializer.data, message="notification found", status_code=200
        )

    def get_one(self, request: Request, id: str, format=None) -> Response:
        """method to get a single notification by id"""
        notiification = get_notification_by_id(id=id)
        if notiification is None:
            return CustomResponse.not_found(
                message="notification is not found", status_code=404
            )

        serializer = NotificationSerializer(notiification)
        if notiification is not None:
            return CustomResponse.success(
                data=serializer.data, message="notification found", status_code=200
            )
        return CustomResponse.not_found(
            message="notification not found", status_code=404
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete a meeting by id"""
        notiifications = get_notification_by_id(id=id)
        if notiifications is not None:
            notiifications.delete()
            return CustomResponse.success(
                message="notification deleted", status_code=204
            )
        return CustomResponse.not_found(
            message="notification not found", status_code=404
        )

    def put(self, request: Request, id: str, format=None) -> Response:
        notiification = get_notification_by_id(id=id)
        if notiification is None:
            return CustomResponse.not_found(message="notification not found")
        serializer = self.get_serializer(notiification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="notification updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="notification failed to update"
        )
