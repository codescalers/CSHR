from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from server.cshr.api.permission import (
    IsAdmin,
    IsSupervisor,
    IsUser,
    UserIsAuthenticated,
)

from server.cshr.api.response import CustomResponse
from server.cshr.models import User
from server.cshr.serializers.users import (
    GeneralUserSerializer,
    SupervisorUserSerializer,
    AdminUserSerializer,
    SelfUserSerializer,
)
from server.cshr.services.users import get_user_by_id


class GeneralUserAPIView(ViewSet, GenericAPIView):
    permission_classes = [IsUser]
    serializer_class = GeneralUserSerializer

    def get_all(self, request: Request) -> Response:
        try:
            users = User.objects.all()
            """if there are no instances """
        except User.DoesNotExist:
            return CustomResponse.not_found(
                message="There are no users found", status_code=404
            )

        serializer = GeneralUserSerializer(users, many=True)
        return CustomResponse.success(
            data=serializer.data, message="show all users", status_code=200
        )

    def get_one(self, request: Request, id: str) -> Response:
        """To get a user by id"""
        user = get_user_by_id(id)
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200,
            )
        return CustomResponse.not_found(message="User not found", status_code=404)


class SupervisorUserAPIView(ViewSet, GenericAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = SupervisorUserSerializer

    def get_all(self, request: Request) -> Response:
        try:
            users = User.objects.all()
            """if there are no instances """
        except User.DoesNotExist:
            return CustomResponse.not_found(
                message="There are no users found", status_code=404
            )

        serializer = self.get_serializer(users, many=True)
        return CustomResponse.success(
            data=serializer.data, message="show all users", status_code=200
        )

    def get_one(self, request: Request, id: str) -> Response:
        """To get a user by id"""
        user = get_user_by_id(id)
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200,
            )
        return CustomResponse.not_found(message="User not found", status_code=404)


class AdminUserAPIView(ViewSet, GenericAPIView):
    """
    * Usage
    admin have full control over a user account
    """

    permission_classes = [IsAdmin]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()

    def get_all(self, request: Request) -> Response:
        try:
            users = User.objects.all()
            """if there are no instances """
        except User.DoesNotExist:
            return CustomResponse.not_found(
                message="There are no users found", status_code=404
            )

        serializer = self.get_serializer(users, many=True)
        return CustomResponse.success(
            data=serializer.data, message="show all users", status_code=200
        )

    def get_one(self, request: Request, id: str) -> Response:
        """To get a user by id"""
        user = get_user_by_id(id)
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200,
            )
        return CustomResponse.not_found(message="User not found", status_code=404)

    def put(self, request: Request, id: str, format=None) -> Response:
        """To update a user"""
        user = get_user_by_id(id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if user is not None:
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(
                    data=serializer.data, status_code=200, message="User updated"
                )
            return CustomResponse.bad_request(
                data=serializer.errors, status_code=400, message="User not updated"
            )
        return CustomResponse.not_found(status_code=404, message="User not found")

    def delete(self, request: Request, id, format=None):
        """To delete a user"""
        user = get_user_by_id(id)
        if user is not None:
            user.delete()
            return CustomResponse.success(message="User deleted", status_code=204)
        return CustomResponse.not_found(status_code=404, message="User not found")


class SelfUserAPIView(ViewSet, GenericAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = SelfUserSerializer
    queryset = User.objects.all()

    def get_one(self, request: Request) -> Response:

        """To get a user by id"""
        try:
            user = self.request.user
            """if there are no instances """
        except User.DoesNotExist:
            return CustomResponse.not_found(
                message="There are no users found", status_code=404
            )

        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200,
            )
        return CustomResponse.not_found(message="User not found", status_code=404)

    def put(self, request: Request, format=None) -> Response:
        """To update a user"""
        try:
            user = self.request.user
            """if there are no instances """
        except User.DoesNotExist:
            return CustomResponse.not_found(
                message="There are no users found", status_code=404
            )
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if user is not None:
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(
                    data=serializer.data, status_code=200, message="User updated"
                )
            return CustomResponse.bad_request(
                data=serializer.errors, status_code=400, message="User not updated"
            )
        return CustomResponse.not_found(status_code=404, message="User not found")
