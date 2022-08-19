from rest_framework.generics import GenericAPIView 
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.office import Office
from rest_framework.viewsets import ViewSet
from ..serializers.office import OfficeSerializer
from ..api.response import CustomResponse
 

class OfficeAPIView(ViewSet,GenericAPIView):
     serializer_class = OfficeSerializer
     queryset= Office.objects.all()
    
     def get_all(self, request: Request) ->  Response:
        offices = self.get_queryset()
        serializer = OfficeSerializer(offices,many=True)
        if offices is not None:
            return CustomResponse.success(
                data=serializer.data,
                message="Offices found",
                status_code=200
            )
        return CustomResponse.not_found(
            message="Office not found",
            status_code=404
        )
     def get_one(self, request: Request, id: str, format=None) ->  Response:
     
        office = Office.objects.get(id=id)
        
        serializer = OfficeSerializer(office)
        if office is not None:
            return CustomResponse.success(
                data=serializer.data,
                message="Offices found",
                status_code=200
            )
        return CustomResponse.not_found(
            message="Office not found",
            status_code=404
        )
     def put(self, request: Request, id: str, format=None) -> Response:
        '''To update an office'''
        office = Office.objects.get(id=id)
        serializer = self.get_serializer(office, data=request.data)
        if office is not None:
             if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(
                    data=serializer.data,
                    status_code=200,
                    message="Office updated"
                )
             return CustomResponse.bad_request(
             data=serializer.errors,
              
             message="Office failed to update"
             )
        return CustomResponse.not_found(
            data=serializer.errors,
            message="Office not found to update"
         )

     def delete(self, request: Request, id, format=None) -> Response:
        ''' To delete an office'''
        office = Office.objects.get(id=id)
        
        if office is not None:
            office.delete()
            return CustomResponse.deleted(
            message="User deleted"
            )
        return CustomResponse.not_found(
        message="Office not found to update"
        )

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