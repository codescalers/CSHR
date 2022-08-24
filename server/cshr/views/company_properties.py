from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.company_properties import Company_properties
from rest_framework.viewsets import ViewSet
from ..serializers.company_properties import CompanyPropertiesSerializer
from ..api.response import CustomResponse
from server.cshr.models.users import User
from server.cshr.api.permission import UserIsAuthenticated
from server.cshr.services.users import get_user_by_id


class CompanyPropertiesAPIView(ViewSet, GenericAPIView):
    """method to get all Company properties"""

    serializer_class = CompanyPropertiesSerializer
    permission_class = UserIsAuthenticated

    def get_all(self, request: Request) -> Response:
        try:
            companyproperties = Company_properties.objects.all()
            """if there are no instances """
        except Company_properties.DoesNotExist:
            return CustomResponse.not_found(
                message="Company propertiess not found", status_code=404
            )

        serializer = CompanyPropertiesSerializer(companyproperties, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Company properties found", status_code=200
        )

    """method to get Company properties by id"""

    def get(self, request: Request, id: str, format=None) -> Response:
        try:
            companyproperties = Company_properties.objects.get(id=id)
        except Company_properties.DoesNotExist:
            return CustomResponse.not_found()

        serializer = CompanyPropertiesSerializer(companyproperties)
        if companyproperties is not None:
            return CustomResponse.success(
                data=serializer.data,
                message="Company properties found",
                status_code=200,
            )
        return CustomResponse.not_found(
            message="Company properties not found", status_code=404
        )

    """method to update a Company properties by id"""

    def put(self, request: Request, id: str, format=None) -> Response:

        try:
            companyproperties = Company_properties.objects.get(id=id)
        except Company_properties.DoesNotExist:
            return CustomResponse.not_found(message="Company properties not found")
        serializer = self.get_serializer(
            companyproperties, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                status_code=200,
                message="Company properties updated",
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Company properties failed to update"
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete Company properties by id"""
        try:
            companyproperties = Company_properties.objects.get(id=id)
        except Company_properties.DoesNotExist:
            return CustomResponse.not_found(message="Company properties not found")
        if companyproperties is not None:
            companyproperties.delete()
            return CustomResponse.success(message="User deleted", status_code=204)
        return CustomResponse.not_found(
            message="Company properties not found to update"
        )

    """method to create a new Company properties"""

    def post(self, request: Request) -> Response:
        """Method to create a new Compensation"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            current_user: User = get_user_by_id(request.user.id)
            serializer.save(user=current_user)
            return CustomResponse.success(
                data=serializer.data,
                message="Company properties is created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Company properties creation failed"
        )
