"""This file contains everything related to the request functionalty."""
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.api.permission import IsAdmin
from server.cshr.api.response import CustomResponse
from server.cshr.models.vacations import Vacation
from server.cshr.serializers.requests import RequestSerializer
from server.cshr.services.requests import get_request_by_id, requests_format_response
from typing import Dict
from server.cshr.models.requests import STATUS_CHOICES, TYPE_CHOICES, Requests
from server.cshr.services.vacations import get_vacation_based_on_request


class RequestApiView(GenericAPIView):
    permission_classes = (IsAdmin,)

    def get(self, request: Request) -> Response:
        res: Dict = requests_format_response()
        return CustomResponse.success(data=res)

class ApproveRequestApiView(GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = (IsAdmin,)

    def put(self, request: Request, id: str) -> Response:
        request_: Requests = get_request_by_id(id)
        if request_ is not None:
            request.data['applying_user'] = request_.applying_user.id
            request.data['approval_user'] = request.user.id
            serializer =  self.get_serializer(data = request.data)
            if serializer.is_valid():
                request_.approval_user = request.user
                request_.status = STATUS_CHOICES.APPROVED,
                request_.save()
                if request_.type == TYPE_CHOICES.VACATIONS:
                    vacation: Vacation = get_vacation_based_on_request(request_)
                    if vacation is not None:
                        # Update change log
                        print("Vacation")
                    return CustomResponse.not_found(message="Vacation not found")
                return CustomResponse.success(message="Request Updated!", data=serializer.data)
            return CustomResponse.bad_request(message="Request data not valid!", error=serializer.errors)
        return CustomResponse.not_found(message="Request not found")
