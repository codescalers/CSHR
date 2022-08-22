from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.office import Office
from rest_framework.viewsets import ViewSet
from ..serializers.office import OfficeSerializer
from ..api.response import CustomResponse


class OfficeAPIView(ViewSet, GenericAPIView):
    serializer_class = OfficeSerializer
    queryset = Office.objects.all()

    def get_all(self, request: Request) -> Response:
        offices = self.get_queryset()
        serializer = OfficeSerializer(offices, many=True)
        if len(offices) != 0:
            return CustomResponse.success(
                data=serializer.data, message="Offices found", status_code=200
            )
        return CustomResponse.not_found(message="Office not found", status_code=404)

    def get(self, request: Request, id: str, format=None) -> Response:
        try:
            office = Office.objects.get(id=id)
        except Office.DoesNotExist:
            return CustomResponse.not_found(message="Office not found", status_code=404)
        serializer = OfficeSerializer(office)
 
        return CustomResponse.success(
                data=serializer.data, message="Offices found", status_code=200
            )
        

    def put(self, request: Request, id: str, format=None) -> Response:
        """To update an office"""
        try:
            office = Office.objects.get(id=id)
        except Office.DoesNotExist:
             return CustomResponse.not_found(
                data=serializer.errors, message="Office not found to update"
        )
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
        """To delete an office"""
        try:       
            office = Office.objects.get(id=id)
        except Office.DoesNotExist:
            return CustomResponse.not_found(message="Office not found to update")
        return CustomResponse.success(message="Office deleted",status_code=204)
        

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