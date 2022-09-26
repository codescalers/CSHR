from server.cshr.utils.redis_functions import get_notifications
from rest_framework.generics import GenericAPIView, ListAPIView
from server.cshr.api.permission import UserIsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from server.cshr.api.response import CustomResponse


class BaseNotificationApiView(ListAPIView, GenericAPIView):
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        res = get_notifications(request.user)
        return CustomResponse.success(data=res)
