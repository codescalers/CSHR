from server.cshr.serializers.hr_letters import hr_letter_serializer
from server.cshr.serializers.hr_letters import hr_letter_update_serializer
from server.cshr.models.hr_letters import HR_LETTERS
from server.cshr.models.users import User
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.api.permission import UserIsAuthenticated, IsAdmin
from server.cshr.services.users import get_user_by_id
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


from server.cshr.api.response import CustomResponse


class HR_Letter_APIView(ViewSet, GenericAPIView):
    """Class HR_Letter_APIVIEW to create a new hr letter into database"""

    serializer_class = hr_letter_serializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Method to create a new hr letter"""
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
                message="Hr letter is created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Hr letter creation failed"
        )

    def get_all(self, request: Request) -> Response:
        hr_letters = HR_LETTERS.objects.all()
        serializer = hr_letter_serializer(hr_letters, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Hr letters found", status_code=200
        )

        """method to get a single HR Letter by id"""

    def get_one(self, request: Request, id: str, format=None) -> Response:
        try:
            hr_letter = HR_LETTERS.objects.get(id=id)
        except HR_LETTERS.DoesNotExist:
            return CustomResponse.not_found(
                message="hr_letter not found", status_code=404
            )

        serializer = hr_letter_serializer(hr_letter)
        if hr_letter is not None:
            return CustomResponse.success(
                data=serializer.data, message="hr_letter found", status_code=200
            )
        return CustomResponse.not_found(message="hr_letter not found", status_code=404)

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete an Hr Letter by id"""
        try:
            hr_letter = HR_LETTERS.objects.get(id=id)
        except HR_LETTERS.DoesNotExist:
            return CustomResponse.not_found(message="hr letter not found")
        if hr_letter is not None:
            hr_letter.delete()
            return CustomResponse.success(message="Hr Letter deleted", status_code=204)
        return CustomResponse.not_found(message="Hr Letter not found")


class HR_Letter_Update_APIView(ViewSet, GenericAPIView):
    serializer_class = hr_letter_update_serializer
    permission_classes = [IsAdmin]

    def put(self, request: Request, id: str, format=None) -> Response:
        try:
            hr_letter = HR_LETTERS.objects.get(id=id)
        except HR_LETTERS.DoesNotExist:
            return CustomResponse.not_found(message="Hr Letter not found")
        serializer = self.get_serializer(hr_letter, data=request.data, partial=True)
        current_user: User = get_user_by_id(request.user.id)
        if serializer.is_valid():
            serializer.save(approval_user=current_user)
            return CustomResponse.success(
                data=serializer.data, status_code=200, message="HR Letter updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="HR Letter failed to update"
        )
