from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from server.cshr.serializers.office import OfficeSerializer
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import ViewSet
from ..api.response import CustomResponse

#     get_all_office
# )
from server.cshr.models.office import Office


class officeApiView(
    ViewSet,
    GenericAPIView,
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    lookup_field = "id"

    def get_all(self, request, *args, **kwargs):
        return CustomResponse.success(
            data=self.list(request, *args, **kwargs).data, message="done"
        )

    def get_one(self, request, *args, **kwargs):
        office = kwargs.get("id")
        if office is not None:
            return CustomResponse.success(
                data=self.retrieve(request, *args, **kwargs).data, message="done"
            )
        return CustomResponse.not_found(message="office not found")

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return CustomResponse.success(
                data=self.create(request, *args, **kwargs).data,
                message="Created",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Can't be created"
        )

    def put(self, request, *args, **kwargs) -> Response:
        office = kwargs.get("id")
        if office is not None:
            instance = self.update(request, *args, **kwargs)
            return CustomResponse.success(
                data=instance.data,
                message="office updated successfully",
                status_code=204,
            )
        return CustomResponse.bad_request(
            error=self.errors, message="office failed to be updated"
        )

    def delete(self, request, *args, **kwargs) -> Response:
        office = kwargs.get("id")
        if office is not None:
            self.destroy(request, *args, **kwargs)
            return CustomResponse.deleted()
        return CustomResponse.bad_request(message="office can't be deleted")
