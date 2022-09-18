from rest_framework.generics import GenericAPIView , ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..serializers.company_properties import CompanyPropertiesSerializer
from ..api.response import CustomResponse
from server.cshr.models.users import User
from server.cshr.api.permission import UserIsAuthenticated
from server.cshr.services.users import get_user_by_id
from server.cshr.services.company_properties import (
    get_all_comopany_properties,
    get_company_properties_by_id,
)


class BaseCompanyPropertiesApiView(ListAPIView, GenericAPIView):
    """method to get all Company properties"""
    serializer_class = CompanyPropertiesSerializer
    permission_class = UserIsAuthenticated

    def get(self, request: Request) -> Response:
        company_properties = get_all_comopany_properties()
        serializer = CompanyPropertiesSerializer(company_properties, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Company properties found", status_code=200
        )

    """method to create a new Company properties"""

    def post(self, request: Request) -> Response:
        """Method to create a new Company properties"""
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
        
        
class CompanyPropertiesApiView(ListAPIView, GenericAPIView):
    serializer_class = CompanyPropertiesSerializer
    permission_class = UserIsAuthenticated
    
    """method to update a Company properties by id"""

    def put(self, request: Request, id: str, format=None) -> Response:

        company_properties = get_company_properties_by_id(id=id)
        if company_properties is None:
            return CustomResponse.not_found(message="Company properties not found")
        serializer = self.get_serializer(
            company_properties, data=request.data, partial=True
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
        company_properties = get_company_properties_by_id(id=id)
        if company_properties is None:
            return CustomResponse.not_found(message="Company properties not found")
        company_properties.delete()
        return CustomResponse.success(message="User deleted", status_code=204)
    
    def get(self, request: Request, id: str, format=None) -> Response:
        """method to get Company properties by id"""
        company_property = get_company_properties_by_id(id=id)
        if company_property is None:
            return CustomResponse.not_found(
                message="Company properties not found", status_code=404
            )

        serializer = CompanyPropertiesSerializer(company_property)
        return CustomResponse.success(
            data=serializer.data,
            message="Company properties found",
            status_code=200,
        )