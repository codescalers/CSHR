from rest_framework.request import Request
from rest_framework.generics import GenericAPIView, ListAPIView

from cshr.utils.redis_functions import (
    http_ensure_redis_error,
    ping_redis,
)
from cshr.api.permission import UserIsAuthenticated
from cshr.api.response import CustomResponse
from cshr.services.notifications import NotificationsService
from cshr.serializers.notification import (
    NotificationSerializer,
    ReadNotificationSerializer,
)
from cshr.models.notification import Notification
from cshr.services.users import get_user_by_id
from cshr.models.users import User


class BaseNotificationApiView(ListAPIView, GenericAPIView):
    permission_classes = (UserIsAuthenticated,)
    serializer_class = NotificationSerializer

    def get(self, request: Request) -> CustomResponse:
        try:
            ping_redis()
        except Exception:
            return http_ensure_redis_error()
        notifications = NotificationsService.filter_based_on_receiver(request.user)
        return CustomResponse.success(
            data=NotificationSerializer(notifications, many=True).data
        )


class ReadNotificationApiView(GenericAPIView):
    permission_classes = (UserIsAuthenticated,)
    serializer_class = ReadNotificationSerializer

    def put(self, request: Request, notification_id: str) -> CustomResponse:
        notification: Notification = NotificationsService.get_by_id(notification_id)
        if notification is None:
            return CustomResponse.not_found(message="Notification is not found.")
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return CustomResponse.success(data=NotificationSerializer(notification).data)

    def get(self, request: Request, notification_id: str) -> CustomResponse:
        notification: Notification = NotificationsService.get_by_id(notification_id)
        if notification is None:
            return CustomResponse.not_found(message="Notification is not found.")
        return CustomResponse.success(data=NotificationSerializer(notification).data)


class ReadAllNotificationsApiView(GenericAPIView):
    permission_classes = (UserIsAuthenticated,)

    def mark_notifications_as_read(self, user: User) -> Notification:
        """Mark all unread notifications for the user as read."""
        notifications = NotificationsService.filter_based_on_receiver(user).filter(
            is_read=False
        )
        notifications.update(is_read=True)
        return NotificationsService.filter_based_on_receiver(user)

    def put(self, request: Request, user_id: str) -> CustomResponse:
        """Handle PUT request to mark all notifications as read for a user."""
        user = get_user_by_id(user_id)
        if not user:
            return CustomResponse.not_found(message="User not found.")

        notifications = self.mark_notifications_as_read(user)
        serialized_notifications = NotificationSerializer(notifications, many=True).data
        return CustomResponse.success(data=serialized_notifications)


class DeleteAllNotificationsApiView(GenericAPIView):
    permission_classes = (UserIsAuthenticated,)

    def delete_notifications(self, user: User) -> Notification:
        """Delete all notifications for the user."""
        notifications = NotificationsService.filter_based_on_receiver(user)
        return notifications.delete()

    def delete(self, request: Request, user_id: str) -> CustomResponse:
        """Handle GET request to mark all notifications as read for a user."""
        user = get_user_by_id(user_id)
        if not user:
            return CustomResponse.not_found(message="User not found.")

        self.delete_notifications(user)
        return CustomResponse.success(data=[])
