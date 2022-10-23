from server.cshr.models.official_documents import OffcialDocument
from server.cshr.serializers.official_documents import OffcialDocumentSerializer

from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.api.permission import (
    IsAdmin,
    IsUser,
)
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.celery.send_email import send_email_for_request
from server.cshr.utils.email_messages_templates import (
    get_official_document_request_email_template,
)

from server.cshr.api.response import CustomResponse
from server.cshr.utils.redis_functions import (
    set_notification_request_redis,
)


class OffcialDocumentAPIView(GenericAPIView):
    """Class OffcialDocument related to user documents, witch document user want from HR"""

    serializer_class = OffcialDocumentSerializer
    permission_classes = [
        IsUser | IsAdmin
    ]

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
                request.user, serializer.data, saved.id
            )
            bool1 = set_notification_request_redis(serializer.data)
            bool2 = send_email_for_request.delay(
                request.user.id, msg, "Hr Letter request"
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
