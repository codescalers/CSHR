from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from ..serializers.compensation import (
    CompensationSerializer,
    CompensationUpdateSerializer,
)
from ..api.response import CustomResponse
from cshr.models.users import User
from cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from cshr.api.permission import (
    IsAdmin,
    IsUser,
    UserIsAuthenticated,
)
from cshr.services.users import get_user_by_id
from cshr.services.compensation import (
    get_all_compensations,
    get_compensation_by_id,
    get_compensations_by_user,
)
from cshr.celery.send_email import send_email_for_request
from cshr.celery.send_email import send_email_for_reply
from cshr.utils.email_messages_templates import (
    get_compensation_reply_email_template,
)
from cshr.utils.email_messages_templates import (
    get_compensation_request_email_template,
)
from cshr.utils.redis_functions import (
    http_ensure_redis_error,
    ping_redis,
    set_notification_request_redis,
    set_notification_reply_redis,
)


class BaseCompensationApiView(ListAPIView, GenericAPIView):
    """method to get all Compensation"""

    serializer_class = CompensationSerializer
    permission_class = UserIsAuthenticated

    def get_queryset(self) -> Response:

        query_set = get_all_compensations()
        return query_set

    """method to create a new Compensation"""

    def post(self, request: Request) -> Response:
        """Method to create a new Compensation"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            current_user: User = get_user_by_id(request.user.id)
            request.data["applying_user"] = current_user.id
            saved = serializer.save(
                type=TYPE_CHOICES.COMPENSATION,
                status=STATUS_CHOICES.PENDING,
                applying_user=current_user,
            )
            msg = get_compensation_request_email_template(
                current_user, serializer.data, saved.id
            )

            try:
                ping_redis()
            except:
                return http_ensure_redis_error()

            bool1 = set_notification_request_redis(serializer.data)
            bool2 = send_email_for_request.delay(
                current_user.id, msg, "Compensation request"
            )
            if bool1 and bool2:
                return CustomResponse.success(
                    data=serializer.data,
                    message="compensation request created",
                    status_code=201,
                )
            else:
                return CustomResponse.not_found(
                    message="user is not found", status_code=404
                )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Compensation creation failed"
        )


class CompensationApiView(ListAPIView, GenericAPIView):

    serializer_class = CompensationSerializer
    permission_class = [
        IsUser,
    ]

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete a Compensation by id"""
        compensation = get_compensation_by_id(id=id)
        if compensation is None:
            return CustomResponse.not_found(message="Compensation not found")
        if compensation.status != STATUS_CHOICES.PENDING:
            return CustomResponse.bad_request(
                message="You can only delete requests with pending status."
            )
        if compensation.applying_user != request.user:
            return CustomResponse.unauthorized()
        compensation.delete()
        return CustomResponse.success(message="Compensation deleted", status_code=204)

    def get(self, request: Request, id: str, format=None) -> Response:
        compensation = get_compensation_by_id(id=id)
        if compensation is None:
            return CustomResponse.not_found(
                message="Compensation not found", status_code=404
            )
        serializer = CompensationSerializer(compensation)
        return CustomResponse.success(
            data=serializer.data, message="Compensation found", status_code=200
        )


class CompensationUserApiView(ListAPIView, GenericAPIView):
    serializer_class = CompensationUpdateSerializer
    permission_classes = [UserIsAuthenticated]

    def get(self, request: Request) -> Response:
        """method to get all compensations for certain user"""
        current_user: User = get_user_by_id(request.user.id)
        if current_user is None:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )
        compensations = get_compensations_by_user(current_user.id)
        serializer = CompensationSerializer(compensations, many=True)
        return CustomResponse.success(
            data=serializer.data, message="compensation requests found", status_code=200
        )


class CompensationUpdateApiView(ListAPIView, GenericAPIView):
    serializer_class = CompensationUpdateSerializer
    permission_classes = [IsUser]
    """method to update a Compensation by id"""

    def put(self, request: Request, id: str, format=None) -> Response:
        compensation = get_compensation_by_id(id=id)
        if compensation is None:
            return CustomResponse.not_found(message="compensation not found")
        serializer = self.get_serializer(compensation, data=request.data, partial=True)
        current_user: User = get_user_by_id(request.user.id)
        if serializer.is_valid():
            serializer.save()
            url = request.build_absolute_uri() + str(serializer.data["id"]) + "/"
            msg = get_compensation_reply_email_template(current_user, compensation, url)
            bool = send_email_for_reply.delay(
                current_user.id,
                compensation.applying_user.id,
                msg,
                "Compensation reply",
            )
            if bool:
                return CustomResponse.success(
                    data=serializer.data,
                    message="compensation request updated",
                    status_code=202,
                )
            else:
                return CustomResponse.not_found(
                    message="user is not found", status_code=404
                )
        return CustomResponse.bad_request(
            data=serializer.errors, message="compensation failed to update"
        )


class CompensationAcceptApiView(ListAPIView, GenericAPIView):
    permission_classes = [IsAdmin]

    def put(self, request: Request, id: str, format=None) -> Response:
        compensation = get_compensation_by_id(id=id)
        if compensation is None:
            return CustomResponse.not_found(message="comopensation not found")
        current_user: User = get_user_by_id(request.user.id)
        compensation.approval_user = current_user
        compensation.status = STATUS_CHOICES.APPROVED
        compensation.save()

        try:
            ping_redis()
        except:
            return http_ensure_redis_error()

        bool1 = set_notification_reply_redis(compensation, "accepted", compensation.id)
        msg = get_compensation_reply_email_template(
            current_user, compensation, compensation.id
        )
        bool2 = send_email_for_reply.delay(
            current_user.id, compensation.applying_user.id, msg, "Compensation reply"
        )
        if bool1 and bool2:
            return CustomResponse.success(
                message="compensation request accepted", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )


class CompensationRejectApiView(ListAPIView, GenericAPIView):
    permission_classes = [IsAdmin]

    def put(self, request: Request, id: str, format=None) -> Response:
        compensation = get_compensation_by_id(id=id)
        if compensation is None:
            return CustomResponse.not_found(message="comopensation not found")
        current_user: User = get_user_by_id(request.user.id)
        compensation.approval_user = current_user
        compensation.status = STATUS_CHOICES.REJECTED
        compensation.save()

        try:
            ping_redis()
        except:
            return http_ensure_redis_error()

        bool1 = set_notification_reply_redis(compensation, "rejected", compensation.id)
        msg = get_compensation_reply_email_template(
            current_user, compensation, compensation.id
        )
        bool2 = send_email_for_reply.delay(
            current_user.id, compensation.applying_user.id, msg, "Compensation reply"
        )
        if bool1 and bool2:
            return CustomResponse.success(
                message="compensation request rejected", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )
