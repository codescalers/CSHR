from server.cshr.serializers.hr_letters import HrLetterSerializer
from server.cshr.serializers.hr_letters import HrLetterUpdateSerializer
from server.cshr.models.users import User
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.api.permission import UserIsAuthenticated, IsAdmin
from server.cshr.services.users import get_user_by_id
from server.cshr.services.hr_letters import get_all_hrLetters, get_hrLetter_by_id
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


from server.cshr.api.response import CustomResponse


class HrLetterApiView(ViewSet, GenericAPIView):
    """Class HR_Letter_APIVIEW to create a new hr letter into database"""

    serializer_class = HrLetterSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Method to create a new hr letter"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            currentUser: User = get_user_by_id(request.user.id)
            serializer.save(
                type=TYPE_CHOICES.HR_LETTERS,
                status=STATUS_CHOICES.PENDING,
                applying_user=currentUser,
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
        hrLetters = get_all_hrLetters()
        serializer = HrLetterSerializer(hrLetters, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Hr letters found", status_code=200
        )

        """method to get a single HR Letter by id"""

    def get_one(self, request: Request, id: str, format=None) -> Response:

        hrLetter = get_hrLetter_by_id(id=id)
        if hrLetter is None:
            return CustomResponse.not_found(
                message="hr_letter not found", status_code=404
            )
        serializer = HrLetterSerializer(hrLetter)
        if hrLetter is not None:
            return CustomResponse.success(
                data=serializer.data, message="hr_letter found", status_code=200
            )
        return CustomResponse.not_found(message="hr_letter not found", status_code=404)

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete an Hr Letter by id"""
        hrLetter = get_hrLetter_by_id(id=id)
        if hrLetter is not None:
            hrLetter.delete()
            return CustomResponse.success(message="Hr Letter deleted", status_code=204)
        return CustomResponse.not_found(message="Hr Letter not found", status_code=404)


class HrLetterUpdateApiView(ViewSet, GenericAPIView):
    serializer_class = HrLetterUpdateSerializer
    permission_classes = [IsAdmin]

    def put(self, request: Request, id: str, format=None) -> Response:
        hrLetter = get_hrLetter_by_id(id=id)
        if hrLetter is None:
            return CustomResponse.not_found(message="Hr Letter not found")
        serializer = self.get_serializer(hrLetter, data=request.data, partial=True)
        currentUser: User = get_user_by_id(request.user.id)
        if serializer.is_valid():
            serializer.save(approval_user=currentUser)
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="HR Letter updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="HR Letter failed to update"
        )
