from typing import List
from server.cshr.serializers.vacations import VacationsSerializer
from server.cshr.serializers.vacations import VacationsUpdateSerializer
from server.cshr.api.permission import UserIsAuthenticated, IsSupervisor
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.models.users import User
from server.cshr.services.users import get_user_by_id
from server.cshr.services.vacations import get_vacation_by_id, get_all_vacations
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.api.response import CustomResponse
from server.cshr.utils.email_messages_templates import (
    get_vacation_request_email_template,
    get_vacation_reply_email_template,
)
from server.cshr.celery.send_email import send_email_for_request
from server.cshr.celery.send_email import send_email_for_reply
from server.cshr.models.vacations import Vacation
from server.cshr.services.vacations import get_vacations_by_user
from server.cshr.utils.redis import set_notification_request_redis


class BaseVacationsApiView(ListAPIView, GenericAPIView):
    """Class Vacations_APIView to create a new vacation into database or get all"""

    serializer_class = VacationsSerializer
    permission_classes = [UserIsAuthenticated]

    def post(self, request: Request) -> Response:
        """Method to create a new vacation request"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            current_user: User = get_user_by_id(request.user.id)
            serializer.save(
                type=TYPE_CHOICES.VACATIONS,
                status=STATUS_CHOICES.PENDING,
                applying_user=current_user,
            )
            url = request.build_absolute_uri() + str(serializer.data["id"]) + "/"
            # to send email async just add .delay after function name as the line below
            # send_email_for_request.delay(current_user.id, serializer.data)
            msg = get_vacation_request_email_template(
                current_user, serializer.data, url
            )
            set_notification_request_redis(serializer.data, url)
            return send_email_for_request(current_user.id, msg, "Vacation request")
        return CustomResponse.bad_request(
            error=serializer.errors, message="vacation request creation failed"
        )

    def get_queryset(self) -> Response:
        """method to get all vacations"""
        query_set: List[Vacation] = get_all_vacations()
        return query_set


class VacationsApiView(ListAPIView, GenericAPIView):
    serializer_class = VacationsSerializer
    permission_classes = [UserIsAuthenticated]
    """Class Vacations_APIView to delete  vacation from database or get certain vacation"""

    def get(self, request: Request, id: str, format=None) -> Response:
        """method to get a single vacation by id"""
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.not_found(
                message="vacation is not found", status_code=404
            )

        serializer = VacationsSerializer(vacation)
        return CustomResponse.success(
            data=serializer.data, message="vacation request found", status_code=200
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete a vacation request by id"""
        vacation = get_vacation_by_id(id=id)
        if vacation is not None:
            vacation.delete()
            return CustomResponse.success(message="Hr Letter deleted", status_code=204)
        return CustomResponse.not_found(message="Hr Letter not found", status_code=404)


class VacationUserApiView(ListAPIView, GenericAPIView):
    serializer_class = VacationsUpdateSerializer
    permission_classes = [UserIsAuthenticated]

    def get(self, request: Request) -> Response:
        """method to get all vacations for certain user"""
        current_user: User = get_user_by_id(request.user.id)
        if current_user is None:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )
        vacations = get_vacations_by_user(current_user.id)
        serializer = VacationsSerializer(vacations, many=True)
        return CustomResponse.success(
            data=serializer.data, message="vacation requests found", status_code=200
        )


class VacationsUpdateApiView(ListAPIView, GenericAPIView):
    serializer_class = VacationsUpdateSerializer
    permission_classes = [IsSupervisor]

    def put(self, request: Request, id: str, format=None) -> Response:
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.not_found(message="Hr Letter not found")
        serializer = self.get_serializer(vacation, data=request.data, partial=True)
        current_user: User = get_user_by_id(request.user.id)
        if serializer.is_valid():
            serializer.save(approval_user=current_user)
            url = request.build_absolute_uri() + str(serializer.data["id"]) + "/"
            # to send email async just add .delay after function name as the line below
            # send_email_for_reply.delay(current_user.id, serializer.data)
            msg = get_vacation_reply_email_template(current_user, serializer.data, url)
            return send_email_for_reply(
                current_user.id, serializer.data, msg, "Vacation reply"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="vacation failed to update"
        )
