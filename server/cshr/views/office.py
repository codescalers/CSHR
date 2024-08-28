from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from cshr.models.office import Office
from cshr.serializers.office import OfficeSerializer
from cshr.api.permission import (
    IsAdmin,
    IsUser,
    IsSupervisor,
    UserIsAuthenticated,
    CustomPermissions,
)
from cshr.services.office import get_office_by_id
from cshr.api.response import CustomResponse
from cshr.models.vacations import PublicHoliday
from cshr.serializers.public_holidays import OfficePublicHolidaySerializer
from django.db.models.query import QuerySet

from cshr.api.pagination import OfficePageHolidaysPagination


class BaseOfficeApiView(ListAPIView, GenericAPIView):
    permission_classes = [UserIsAuthenticated | IsUser | IsAdmin | IsSupervisor]
    serializer_class = OfficeSerializer

    def get_queryset(self) -> Response:
        query_set = Office.objects.all()
        return query_set

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


class OfficeApiView(ListAPIView, GenericAPIView):
    permission_classes = [UserIsAuthenticated | IsUser | IsAdmin | IsSupervisor]
    serializer_class = OfficeSerializer

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

    def put(self, request: Request, id: str, format=None) -> Response:
        """To update an office"""
        has_permission = CustomPermissions.admin_or_supervisor(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        office = get_office_by_id(id)

        if office is not None:
            serializer = OfficeSerializer(office, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(
                    data=serializer.data, status_code=202, message="Office updated"
                )
            return CustomResponse.bad_request(
                error=serializer.errors, message="Office failed to update"
            )
        return CustomResponse.not_found(message="Office not found to update")

class GetOfficePublicHolidaysBasedOnYearAPIView(ListAPIView, GenericAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = OfficePublicHolidaySerializer
    pagination_class = OfficePageHolidaysPagination

    def get_holidays(self, office_id: int, year: int) -> QuerySet:
        """
        Retrieve public holidays for a specific office and year.
        """
        office = Office.objects.filter(id=office_id).first()
        if not office:
            raise NotFound(detail={"message": "Office does not exist."})

        holidays = PublicHoliday.objects.filter(
            location=office,
            holiday_date__year=year
        ).select_related("location")
        
        return holidays

    def get_queryset(self) -> QuerySet:
        office_id = self.request.query_params.get('office_id')
        year = self.request.query_params.get('year')

        if not office_id or not year:
            raise ValidationError(detail={"message": "Both office_id and year are required."})

        try:
            office_id = int(office_id)
            year = int(year)
        except ValueError:
            raise ValidationError(detail={
                "message": "The office_id and year parameters should be integers."
            })

        return self.get_holidays(office_id, year)

    def list(self, request, *args, **kwargs) -> Response:
        """
        Override the list method to provide a custom response structure.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(data=serializer.data)