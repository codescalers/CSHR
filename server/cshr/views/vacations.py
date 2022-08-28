from server.cshr.serializers.vacations import vacations_serializer
from server.cshr.serializers.vacations import vacations_update_serializer
from server.cshr.api.permission import UserIsAuthenticated, IsAdmin
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.models.users import User
from server.cshr.models.vacations import Vacation
from server.cshr.services.users import get_user_by_id

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from server.cshr.api.response import CustomResponse


class Vacations_APIView(ViewSet, GenericAPIView):
    """Class Vacations_APIView to create a new vacation into database"""

    serializer_class = vacations_serializer
    permission_classes = [UserIsAuthenticated]

    def post(self, request: Request) -> Response:
        """Method to create a new vacation request"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            current_user: User = get_user_by_id(request.user.id)
            serializer.save(
                type=TYPE_CHOICES.HR_LETTERS,
                status=STATUS_CHOICES.PENDING,
                applying_user=current_user,
            )
            return CustomResponse.success(
                data=serializer.data,
                message="vacation request is created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="vacation request creation failed"
        )

    def get_all(self, request: Request) -> Response:
        vacations = Vacation.objects.all()
        serializer = vacations_serializer(vacations, many=True)
        return CustomResponse.success(
            data=serializer.data, message="vacation requests found", status_code=200
        )

        """method to get a single HR Letter by id"""

    def get_one(self, request: Request, id: str, format=None) -> Response:
        try:
            vacation = Vacation.objects.get(id=id)
        except Vacation.DoesNotExist:
            return CustomResponse.not_found()

        serializer = vacations_serializer(vacation)
        if vacation is not None:
            return CustomResponse.success(
                data=serializer.data, message="vacation request found", status_code=200
            )
        return CustomResponse.not_found(
            message="vacation request not found", status_code=404
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete a vacation request by id"""
        try:
            vacation = Vacation.objects.get(id=id)
        except Vacation.DoesNotExist:
            return CustomResponse.not_found(message="hr letter not found")
        if vacation is not None:
            vacation.delete()
            return CustomResponse.success(message="Hr Letter deleted", status_code=204)
        return CustomResponse.not_found(message="Hr Letter not found")


class Vacations_Update_APIView(ViewSet, GenericAPIView):
    serializer_class = vacations_update_serializer
    permission_classes = [IsAdmin]

    def put(self, request: Request, id: str, format=None) -> Response:
        try:
            vacation = Vacation.objects.get(id=id)
        except Vacation.DoesNotExist:
            return CustomResponse.not_found(message="Hr Letter not found")
        serializer = self.get_serializer(vacation, data=request.data, partial=True)
        current_user: User = get_user_by_id(request.user.id)
        if serializer.is_valid():
            serializer.save(approval_user=current_user)
            return CustomResponse.success(
                data=serializer.data, status_code=200, message="vacation updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="vacation failed to update"
        )
