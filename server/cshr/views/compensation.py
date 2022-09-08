from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..serializers.compensation import CompensationSerializer
from ..api.response import CustomResponse
from server.cshr.models.users import User
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.api.permission import UserIsAuthenticated
from server.cshr.services.users import get_user_by_id
from server.cshr.services.compensation import (
    get_all_compensations,
    get_compensation_by_id,
)
from server.cshr.celery.send_email import send_email_for_compensation_request


class CompensationApiView(ViewSet, GenericAPIView):
    """method to get all Compensation"""

    serializer_class = CompensationSerializer
    permission_class = UserIsAuthenticated

    def get_all(self, request: Request) -> Response:

        compensation = get_all_compensations()

        serializer = CompensationSerializer(compensation, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Compensation found", status_code=200
        )

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

    """method to update a Compensation by id"""

    def put(self, request: Request, id: str, format=None) -> Response:

        compensation = get_compensation_by_id(id=id)
        if compensation is None:
            return CustomResponse.not_found(message="Compensation not found")
        serializer = self.get_serializer(compensation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data, status_code=200, message="Compensation updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Compensation failed to update"
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete a Compensation by id"""
        compensation = get_compensation_by_id(id=id)
        if compensation is None:
            return CustomResponse.not_found(message="Compensation not found")

        compensation.delete()
        return CustomResponse.success(message="User deleted", status_code=204)

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
            send_email_for_compensation_request(current_user, serializer.data)
            return CustomResponse.success(
                data=serializer.data,
                message="Compensation is created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Compensation creation failed"
        )
