from cshr.models.official_documents import OffcialDocument
from cshr.models.users import User
from cshr.serializers.official_documents import OffcialDocumentSerializer

from cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from cshr.api.permission import (
    IsAdmin,
    IsUser,
)
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from cshr.celery.send_email import send_email_for_reply, send_email_for_request
from cshr.services.official_documents import get_official_document_by_id
from cshr.services.users import get_user_by_id
from cshr.utils.email_messages_templates import (
    get_official_document_request_email_template,
)

from cshr.api.response import CustomResponse
from cshr.utils.redis_functions import (
    http_ensure_redis_error,
    ping_redis,
    set_notification_reply_redis,
    set_notification_request_redis,
)


class OffcialDocumentAPIView(GenericAPIView):
    """Class OffcialDocument related to user documents, witch document user want from HR"""

    serializer_class = OffcialDocumentSerializer
    permission_classes = [IsUser | IsAdmin]

    def post(self, request: Request) -> Response:
        """Use this endpoint to post new document request."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            saved = serializer.save(
                applying_user=request.user,
                status=STATUS_CHOICES.PENDING,
                type=TYPE_CHOICES.OFFICIAL_DOCUMENT,
            )
            msg = get_official_document_request_email_template(
                request.user, saved, saved.id
            )

            try:
                ping_redis()
            except:
                return http_ensure_redis_error()

            bool1 = set_notification_request_redis(serializer.data)
            bool2 = send_email_for_request.delay(
                request.user.id, msg, "Official Document request"
            )

            if bool1 and bool2:
                return CustomResponse.success(
                    message="Document saved successfully", data=serializer.data
                )
            return CustomResponse.bad_request(
                message="Error while sending notifications"
            )
        return CustomResponse.bad_request(
            message="Please make suee that you entred a valid date.",
            error=serializer.errors,
        )

    def get_queryset(self):
        """Return all documents"""
        return OffcialDocument.objects.all()


class OfficialDocumentAcceptApiView(GenericAPIView):
    permission_classes = [
        IsAdmin,
    ]

    def put(self, request: Request, id: str, format=None) -> Response:
        document = get_official_document_by_id(id=id)
        if document is None:
            return CustomResponse.not_found(
                message="Official Document request not found"
            )
        current_user: User = get_user_by_id(request.user.id)
        document.approval_user = current_user
        document.status = STATUS_CHOICES.APPROVED
        document.save()

        try:
            ping_redis()
        except:
            return http_ensure_redis_error()

        bool1 = set_notification_reply_redis(document, "accepted", document.id)
        msg = get_official_document_request_email_template(
            current_user, document, document.id
        )
        bool2 = send_email_for_reply.delay(
            current_user.id, document.applying_user.id, msg, "Official Document reply"
        )
        if bool1 and bool2:
            return CustomResponse.success(
                message="Official Document request accepted", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )


class OfficialDocumentRejectApiView(GenericAPIView):
    permission_classes = [
        IsAdmin,
    ]

    def put(self, request: Request, id: str, format=None) -> Response:
        document = get_official_document_by_id(id=id)
        if document is None:
            return CustomResponse.not_found(message="Hr Letter not found")
        current_user: User = get_user_by_id(request.user.id)
        document.approval_user = current_user
        document.status = STATUS_CHOICES.REJECTED
        document.save()
        bool1 = set_notification_reply_redis(document, "rejected", document.id)
        msg = get_official_document_request_email_template(
            current_user, document, document.id
        )
        bool2 = send_email_for_reply.delay(
            current_user.id, document.applying_user.id, msg, "Hr Letter reply"
        )
        if bool1 and bool2:
            return CustomResponse.success(
                message="hr letter request rejected", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )
