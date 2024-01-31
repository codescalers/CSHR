from cshr.utils.redis_functions import get_notifications, get_redis_conf, ping_redis
from rest_framework.generics import GenericAPIView, ListAPIView
from cshr.api.permission import UserIsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from cshr.api.response import CustomResponse


class BaseNotificationApiView(ListAPIView, GenericAPIView):
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        redis_conf = get_redis_conf()
        try:
            ping_redis()
        except:
            return CustomResponse.bad_request(
                message="Connection Refused",
                error={
                    "message": "Redis is not running, please make sure that you run the Redis server on the provided values",
                    "values": {"host": redis_conf.get('host'), "port": redis_conf.get('port')},
                },
            )
        res = get_notifications(request.user)
        return CustomResponse.success(data=res)
