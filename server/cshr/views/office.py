from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.office import Office
from rest_framework.viewsets import ViewSet
from ..serializers.office import OfficeSerializer
from ..api.response import CustomResponse


class OfficeAPIView(ViewSet, GenericAPIView):
    """method to get all Offices"""

    def get_all(self, request: Request) -> Response:
        try:
            offices = Office.objects.all()
            """if there are no instances """
        except Office.DoesNotExist:
            return CustomResponse.not_found(message="Office not found", status_code=404)

        serializer = OfficeSerializer(offices, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Offices found", status_code=200
        )

    """method to get a single Office by id"""

    def get(self, request: Request, id: str, format=None) -> Response:
        try:
            office = Office.objects.get(id=id)
        except Office.DoesNotExist:
            print("hi")
            return CustomResponse.not_found()

        serializer = OfficeSerializer(office)
        if office is not None:
            return CustomResponse.success(
                data=serializer.data, message="Offices found", status_code=200
            )
        return CustomResponse.not_found(message="Office not found", status_code=404)

    """method to update an office by id"""

    def put(self, request: Request, id: str, format=None) -> Response:

        try:
            office = Office.objects.get(id=id)
        except Office.DoesNotExist:
            return CustomResponse.not_found(message="Office not found")
        serializer = self.get_serializer(office, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data, status_code=200, message="Office updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Office failed to update"
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete an office by id"""
        try:
            office = Office.objects.get(id=id)
        except Office.DoesNotExist:
            return CustomResponse.not_found(message="Office not found")
        if office is not None:
            office.delete()
            return CustomResponse.deleted(message="User deleted")
        return CustomResponse.not_found(message="Office not found to update")

    """method to create a new office"""

    def post(self, request: Request) -> Response:
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
