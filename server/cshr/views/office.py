from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.office import Office
from rest_framework.viewsets import ViewSet
from ..serializers.office import OfficeSerializer
from ..api.response import CustomResponse
from server.cshr.api.permission import (
    IsAdmin,
    IsUser,
    IsSupervisor,
    UserIsAuthenticated,
    CustomPermissions,
)
from server.cshr.services.office import get_office_by_id


class OfficeAPIView(ViewSet, GenericAPIView):
    queryset = Office.objects.all()
    permission_classes = [UserIsAuthenticated | IsUser | IsAdmin | IsSupervisor]
    serializer_class = OfficeSerializer

    def patch(self, request: Request, id: str, format=None) -> Response:
        """To update an office"""
        has_permission = CustomPermissions.admin_or_supervisor(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        office = get_office_by_id(id)

        if office is not None:
            serializer = OfficeSerializer(office, data=request.data, partial=True)
            if (
                "name" in request.data
                and request.data["name"] is not None
                or "country" in request.data
                and request.data["country"] is not None
            ):
                if serializer.is_valid():
                    serializer.save()
                    return CustomResponse.success(
                        data=serializer.data, status_code=202, message="Office updated"
                    )
            return CustomResponse.bad_request(message="Office failed to update")
        return CustomResponse.not_found(message="Office not found to update")

    def get_all(self, request: Request) -> Response:
        offices = self.get_queryset()
        serializer = OfficeSerializer(offices, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Offices found", status_code=200
        )

    def get(self, request: Request, id: str, format=None) -> Response:
        office = get_office_by_id(id)
        if office is None:
            return CustomResponse.not_found(message="Office not found", status_code=404)
        serializer = OfficeSerializer(office)

        return CustomResponse.success(
            data=serializer.data, message="Offices found", status_code=200
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """To delete an office"""
        has_permission = CustomPermissions.admin(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        office = get_office_by_id(id)
        if office is not None:
            office.delete()
            return CustomResponse.success(message="Office deleted", status_code=204)
        return CustomResponse.not_found(message="Office not found to delete")

    def post(self, request: Request) -> Response:
        has_permission = CustomPermissions.admin(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Office created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Office creation failed"
        )
