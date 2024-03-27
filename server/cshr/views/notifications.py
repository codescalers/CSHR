from cshr.utils.redis_functions import get_notifications, http_ensure_redis_error, ping_redis
from rest_framework.generics import GenericAPIView, ListAPIView
from cshr.api.permission import UserIsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from cshr.api.response import CustomResponse


class BaseNotificationApiView(ListAPIView, GenericAPIView):
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        try:
            ping_redis()
        except:
            return http_ensure_redis_error()
        res = get_notifications(request.user)
        return CustomResponse.success(data=res)
