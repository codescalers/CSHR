from server.cshr.serializers.hr_letters import (
    HrLetterSerializer,
    LandingPageHrLetterSerializer,
    UserDocumentsSerializer,
)
from server.cshr.serializers.hr_letters import HrLetterUpdateSerializer
from server.cshr.models.users import User
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.api.permission import (
    IsAdmin,
    UserIsAuthenticated,
    IsSupervisor,
)
from server.cshr.services.users import get_user_by_id
from server.cshr.services.hr_letters import (
    filter_all_docs_based_on_user,
    get_all_hrLetters,
    get_hrLetter_by_id,
)
from server.cshr.services.hr_letters import get_hr_letter_by_user
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.celery.send_email import send_email_for_reply, send_email_for_request
from server.cshr.utils.email_messages_templates import (
    get_hr_letter_request_email_template,
)
from server.cshr.utils.email_messages_templates import (
    get_hr_letter_reply_email_template,
)

from server.cshr.api.response import CustomResponse
from server.cshr.utils.redis_functions import (
    set_notification_request_redis,
    set_notification_reply_redis,
)


class BaseHrLetterApiView(ListAPIView, GenericAPIView):
    """Class HR_Letter_APIVIEW to create a new hr letter into database"""

    serializer_class = HrLetterSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Method to create a new hr letter"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            with_date: bool = serializer.validated_data.get("from_date")
            end_date: bool = serializer.validated_data.get("end_date")
            if with_date and with_date is None or with_date and end_date is None:
                return CustomResponse.bad_request(
                    message="If you want to mention the date you have to send it with your request"
                )
            current_user: User = get_user_by_id(request.user.id)
            saved = serializer.save(
                type=TYPE_CHOICES.HR_LETTERS,
                status=STATUS_CHOICES.PENDING,
                applying_user=current_user,
            )
            msg = get_hr_letter_request_email_template(
                current_user, serializer.data, saved.id
            )
            bool1 = set_notification_request_redis(serializer.data)
            bool2 = send_email_for_request.delay(
                current_user.id, msg, "Hr Letter request"
            )
            if bool1 and bool2:
                return CustomResponse.success(
                    data=serializer.data,
                    message="hr letter request created",
                    status_code=201,
                )
            else:
                return CustomResponse.not_found(
                    message="user is not found", status_code=404
                )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Hr letter creation failed"
        )

    def get_queryset(self) -> Response:
        query_set = get_all_hrLetters()
        return query_set


class BaseUserDocumentsAPIView(ListAPIView, GenericAPIView):
    """Class BaseUserDocumentsAPIView to create a new user document into database"""

    serializer_class = UserDocumentsSerializer
    permission_classes = (IsAdmin,)

    def post(self, request: Request) -> Response:
        """Method to create a new user document"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Document created",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Document creation failed"
        )

    def get_queryset(self) -> Response:
        query_set = get_all_hrLetters()
        return query_set


class HrLetterApiView(ListAPIView, GenericAPIView):

    serializer_class = LandingPageHrLetterSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, id: str, format=None) -> Response:
        """method to get a single HR Letter by id"""
        hr_letter = get_hrLetter_by_id(id=id)
        if hr_letter is None:
            return CustomResponse.not_found(
                message="hr_letter not found", status_code=404
            )
        serializer = self.get_serializer(hr_letter)

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


class HrLetterUserApiView(ListAPIView, GenericAPIView):
    serializer_class = HrLetterUpdateSerializer
    permission_classes = [UserIsAuthenticated]

    def get(self, request: Request) -> Response:
        """method to get all Hr Letters for certain user"""
        current_user: User = get_user_by_id(request.user.id)
        if current_user is None:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )
        hr_letters = get_hr_letter_by_user(current_user.id)
        serializer = HrLetterSerializer(hr_letters, many=True)
        return CustomResponse.success(
            data=serializer.data, message="hr letter requests found", status_code=200
        )


class HrLetterUpdateApiView(ListAPIView, GenericAPIView):
    serializer_class = HrLetterUpdateSerializer
    permission_classes = [IsSupervisor]

    def put(self, request: Request, id: str, format=None) -> Response:
        hr_letter = get_hrLetter_by_id(id=id)
        if hr_letter is None:
            return CustomResponse.not_found(message="Hr Letter not found")
        serializer = self.get_serializer(hr_letter, data=request.data, partial=True)
        current_user: User = get_user_by_id(request.user.id)
        if serializer.is_valid():
            serializer.save(approval_user=current_user)
            url = request.build_absolute_uri() + str(serializer.data["id"]) + "/"
            msg = get_hr_letter_reply_email_template(current_user, hr_letter, url)
            bool = send_email_for_reply.delay(
                current_user.id, hr_letter.applying_user.id, msg, "Hr Letter reply"
            )
            if bool:
                return CustomResponse.success(
                    data=serializer.data,
                    message="hr letter request updated",
                    status_code=202,
                )
            else:
                return CustomResponse.not_found(
                    message="user is not found", status_code=404
                )
        return CustomResponse.bad_request(
            data=serializer.errors, message="HR Letter failed to update"
        )


class HrLetterAcceptApiView(ListAPIView, GenericAPIView):
    permission_classes = [
        IsAdmin,
    ]

    def put(self, request: Request, id: str, format=None) -> Response:
        hr_letter = get_hrLetter_by_id(id=id)
        if hr_letter is None:
            return CustomResponse.not_found(message="Hr Letter not found")
        current_user: User = get_user_by_id(request.user.id)
        hr_letter.approval_user = current_user
        hr_letter.status = STATUS_CHOICES.APPROVED
        hr_letter.save()
        bool1 = set_notification_reply_redis(hr_letter, "accepted", hr_letter.id)
        msg = get_hr_letter_reply_email_template(current_user, hr_letter, hr_letter.id)
        bool2 = send_email_for_reply.delay(
            current_user.id, hr_letter.applying_user.id, msg, "Hr Letter reply"
        )
        if bool1 and bool2:
            return CustomResponse.success(
                message="hr letter request accepted", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )


class HrLetterRejectApiView(ListAPIView, GenericAPIView):
    permission_classes = [
        IsAdmin,
    ]

    def put(self, request: Request, id: str, format=None) -> Response:
        hr_letter = get_hrLetter_by_id(id=id)
        if hr_letter is None:
            return CustomResponse.not_found(message="Hr Letter not found")
        current_user: User = get_user_by_id(request.user.id)
        hr_letter.approval_user = current_user
        hr_letter.status = STATUS_CHOICES.REJECTED
        hr_letter.save()
        url = request.build_absolute_uri()
        bool1 = set_notification_reply_redis(hr_letter, "rejected", hr_letter.id)
        msg = get_hr_letter_reply_email_template(current_user, hr_letter, hr_letter.id)
        bool2 = send_email_for_reply.delay(
            current_user.id, hr_letter.applying_user.id, msg, "Hr Letter reply"
        )
        if bool1 and bool2:
            return CustomResponse.success(
                message="hr letter request rejected", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )


class GetAllUserDocumentsAPIView(ListAPIView):
    permission_classes = [IsAdmin | IsSupervisor]
    serializer_class = UserDocumentsSerializer

    def get(self, request: Request, user_id: str) -> Response:
        if not user_id.isdigit():
            return CustomResponse.bad_request(
                message="Invalid id", error="Id must be a number", data=[]
            )
        user = get_user_by_id(user_id)
        if user is None:
            return CustomResponse.not_found(
                message=f"There is no user has this id {user_id}"
            )
        queryset = filter_all_docs_based_on_user(user)
        return CustomResponse.success(
            data=self.get_serializer(queryset, many=True).data
        )
