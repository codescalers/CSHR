from server.cshr.serializers.notifications import NotificationsSerializer
from server.cshr.utils.redis_functions import get_notifications
from rest_framework.generics import ListAPIView
from server.cshr.api.permission import UserIsAuthenticated


class BaseNotificationApiView(ListAPIView):
    permission_classes = (UserIsAuthenticated,)
    serializer_class = NotificationsSerializer
    # TODO: Create new serializer here.

    def get_queryset(self):
        return get_notifications(self.request.user)
