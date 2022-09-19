from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from ..serializers.compensation import (
    CompensationSerializer,
    CompensationUpdateSerializer,
)
from ..api.response import CustomResponse
from server.cshr.models.users import User
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.api.permission import UserIsAuthenticated, IsSupervisor
from server.cshr.services.users import get_user_by_id
from server.cshr.services.compensation import (
    get_all_compensations,
    get_compensation_by_id,
    get_compensations_by_user,
)
from server.cshr.celery.send_email import send_email_for_request
from server.cshr.celery.send_email import send_email_for_reply
from server.cshr.utils.email_messages_templates import (
    get_compensation_reply_email_template,
)
from server.cshr.utils.email_messages_templates import (
    get_compensation_request_email_template,
)


class BaseCompensationApiView(ListAPIView, GenericAPIView):
    """method to get all Compensation"""

    serializer_class = CompensationSerializer
    permission_class = UserIsAuthenticated

    def get(self, request: Request) -> Response:

        compensation = get_all_compensations()

        serializer = CompensationSerializer(compensation, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Compensation found", status_code=200
        )

    """method to create a new Compensation"""

    def post(self, request: Request) -> Response:
        """Method to create a new Compensation"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            current_user: User = get_user_by_id(request.user.id)
            serializer.save(
                type=TYPE_CHOICES.COMPENSATION,
                status=STATUS_CHOICES.PENDING,
                applying_user=current_user,
            )
            url = request.build_absolute_uri() + str(serializer.data["id"]) + "/"
            # to send email async just add .delay after function name as the line below
            # send_email_for_request.delay(current_user.id, serializer.data)
            msg = get_compensation_request_email_template(
                current_user, serializer.data, url
            )
            return send_email_for_request(current_user.id, msg, "Compensation request")
        return CustomResponse.bad_request(
            error=serializer.errors, message="Compensation creation failed"
        )


class CompensationApiView(ListAPIView, GenericAPIView):

    serializer_class = CompensationSerializer
    permission_class = UserIsAuthenticated

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete a Compensation by id"""
        compensation = get_compensation_by_id(id=id)
        if compensation is None:
            return CustomResponse.not_found(message="Compensation not found")

        compensation.delete()
        return CustomResponse.success(message="User deleted", status_code=204)
        """method to get a single Compensation by id"""

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
    permission_classes = [IsSupervisor]
    """method to update a Compensation by id"""

    def put(self, request: Request, id: str, format=None) -> Response:
        compensation = get_compensation_by_id(id=id)
        if compensation is None:
            return CustomResponse.not_found(message="compensation not found")
        serializer = self.get_serializer(compensation, data=request.data, partial=True)
        current_user: User = get_user_by_id(request.user.id)
        if serializer.is_valid():
            serializer.save(approval_user=current_user)
            url = request.build_absolute_uri() + str(serializer.data["id"]) + "/"
            # to send email async just add .delay after function name as the line below
            # send_email_for_reply.delay(current_user.id, serializer.data)
            msg = get_compensation_reply_email_template(
                current_user, serializer.data, url
            )
            return send_email_for_reply(
                current_user.id, serializer.data, msg, "Compensation reply"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="compensation failed to update"
        )
