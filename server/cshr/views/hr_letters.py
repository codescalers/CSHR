from server.cshr.serializers.hr_letters import HrLetterSerializer
from server.cshr.serializers.hr_letters import HrLetterUpdateSerializer
from server.cshr.models.users import User
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.api.permission import UserIsAuthenticated, IsAdmin
from server.cshr.services.users import get_user_by_id
from server.cshr.services.hr_letters import get_all_hrLetters, get_hrLetter_by_id
from rest_framework.generics import GenericAPIView , ListAPIView
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from server.cshr.celery.send_email import send_email_for_hr_letter_reply
from server.cshr.celery.send_email import send_email_for_hr_letter_request

from server.cshr.api.response import CustomResponse


class BaseHrLetterApiView(ListAPIView, GenericAPIView):
    """Class HR_Letter_APIVIEW to create a new hr letter into database"""

    serializer_class = HrLetterSerializer
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
            send_email_for_hr_letter_request(current_user, serializer.data)
            return CustomResponse.success(
                data=serializer.data,
                message="Hr letter is created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Hr letter creation failed"
        )

    def get(self, request: Request) -> Response:
        hrLetters = get_all_hrLetters()
        serializer = HrLetterSerializer(hrLetters, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Hr letters found", status_code=200
        )

       



class HrLetterApiView(ListAPIView, GenericAPIView):
    
    serializer_class = HrLetterSerializer
    permission_classes = (UserIsAuthenticated,)
    
    
    def get(self, request: Request, id: str, format=None) -> Response:
        """method to get a single HR Letter by id"""
        hr_letter = get_hrLetter_by_id(id=id)
        if hr_letter is None:
            return CustomResponse.not_found(
                message="hr_letter not found", status_code=404
            )
        serializer = HrLetterSerializer(hr_letter)

        return CustomResponse.success(
            data=serializer.data, message="hr_letter found", status_code=200
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete an Hr Letter by id"""
        hr_letter = get_hrLetter_by_id(id=id)
        if hr_letter is not None:
            hr_letter.delete()
            return CustomResponse.success(message="Hr Letter deleted", status_code=204)
        return CustomResponse.not_found(message="Hr Letter not found", status_code=404)
    
class HrLetterUpdateApiView(ListAPIView, GenericAPIView):
    serializer_class = HrLetterUpdateSerializer
    permission_classes = [IsAdmin]

    def put(self, request: Request, id: str, format=None) -> Response:
        hr_letter = get_hrLetter_by_id(id=id)
        if hr_letter is None:
            return CustomResponse.not_found(message="Hr Letter not found")
        serializer = self.get_serializer(hr_letter, data=request.data, partial=True)
        current_user: User = get_user_by_id(request.user.id)
        if serializer.is_valid():
            serializer.save(approval_user=current_user)
            send_email_for_hr_letter_reply(current_user, serializer.data)
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="HR Letter updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="HR Letter failed to update"
        )
