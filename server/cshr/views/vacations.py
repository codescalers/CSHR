from server.cshr.serializers.vacations import VacationsSerializer
from server.cshr.serializers.vacations import VacationsUpdateSerializer
from server.cshr.api.permission import UserIsAuthenticated, IsSupervisor
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.models.users import User
from server.cshr.services.users import get_user_by_id
from server.cshr.services.vacations import get_vacation_by_id, get_all_vacations
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from server.cshr.celery.send_email import send_email_for_vacation_reply
from server.cshr.celery.send_email import send_email_for_vacation_request
from server.cshr.api.response import CustomResponse


class VacationsApiView(ViewSet, GenericAPIView):
    """Class Vacations_APIView to create a new vacation into database"""

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
            # to send email async just add .delay after function name as the line below
            # send_email_for_vacation_request.delay(current_user.id, serializer.data)
            send_email_for_vacation_request(current_user.id, serializer.data)
            return CustomResponse.success(
                data=serializer.data,
                message="vacation request is created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="vacation request creation failed"
        )

    def get_all(self, request: Request) -> Response:
        vacations = get_all_vacations()
        serializer = VacationsSerializer(vacations, many=True)
        return CustomResponse.success(
            data=serializer.data, message="vacation requests found", status_code=200
        )

        """method to get a single HR Letter by id"""

    def get_one(self, request: Request, id: str, format=None) -> Response:

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


class VacationsUpdateApiView(ViewSet, GenericAPIView):
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
            # to send email async just add .delay after function name as the line below
            # send_email_for_vacation_reply.delay(current_user.id, serializer.data)
            send_email_for_vacation_reply(current_user.id, serializer.data)
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="vacation updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="vacation failed to update"
        )
