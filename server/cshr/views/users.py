from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from server.cshr.api.response import CustomResponse
from server.cshr.models import User
from server.cshr.serializers.users import UserSerializer
from server.cshr.services.users import get_user_by_id


class UserAPIView(GenericAPIView):
    """
    * Usage
    Class UserAPIView has all the functionality based of the User
    Methods [GET, PUT, DELETE]
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_all(self, request: Request) -> Response:
        """To get all users"""
        user = self.get_queryset()
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="Users found",
                status_code=200
            )
        return CustomResponse.not_found(
            message="User not found",
            status_code=404
        )

    def get_one(self, request: Request, pk: str) -> Response:
        '''To get a user by id'''
        user = get_user_by_id(pk)
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200
            )
        return CustomResponse.not_found(
            message="User not found",
            status_code=404
        )

    def post(self, request: Request, format=None):
        '''To create a user'''
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                status_code=201,
                message="User created")
        return CustomResponse.bad_request(
            data=serializer.errors,
            status_code=400,
            message="User not created")

    def put(self, request: Request, pk: str, format=None) -> Response:
        '''To update a user'''
        user = get_user_by_id(pk)
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                status_code=200,
                message="User updated")
        return CustomResponse.bad_request(
            data=serializer.errors,
            status_code=400,
            message="User not updated")

    def delete(self, request: Request, pk, format=None):
        ''' To delete a user'''
        user = self.get_object(pk)
        if user is not None:
            user.delete()
            return CustomResponse.deleted(
                status_code=204,
                message="User deleted")
        return CustomResponse.not_found(
            status_code=404,
            message="User not found")
