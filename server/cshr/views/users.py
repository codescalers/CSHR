from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from server.cshr.api.permission import (
    IsAdmin,
    IsSupervisor,
    UserIsAuthenticated,
)
from server.cshr.utils.validations import Validator
from server.cshr.api.response import CustomResponse
from server.cshr.serializers.users import (
    GeneralUserSerializer,
    SupervisorUserSerializer,
    AdminUserSerializer,
    SelfUserSerializer,
    UserSkillsSerializer,
)
from server.cshr.services.users import (
    get_user_by_id,
    get_or_create_skill_by_name,
    get_all_of_users,
)


class GeneralUserAPIView(ViewSet, GenericAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = GeneralUserSerializer

    def get_all(self, request: Request) -> Response:
        """get all users in the system for a normal user"""
        users = get_all_of_users()
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


class SupervisorUserAPIView(ViewSet, GenericAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = SupervisorUserSerializer

    def get_all(self, request: Request) -> Response:
        """get all users in the system for a supervisor"""
        users = get_all_of_users()
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
    admin have full control over a user account
    """

    permission_classes = [IsAdmin]
    serializer_class = AdminUserSerializer

    def get_all(self, request: Request) -> Response:
        """get all users in the system for an admin"""
        users = get_all_of_users()
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
                    data=serializer.data, status_code=204, message="User updated"
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

    def get_one(self, request: Request) -> Response:

        """To get a user by id"""

        user = self.request.user
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200,
            )
        return CustomResponse.not_found(message="User not found", status_code=404)

    def put(self, request: Request, format=None) -> Response:
        """To update a user"""
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if user is not None:
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(
                    data=serializer.data, status_code=204, message="User updated"
                )
            return CustomResponse.bad_request(
                data=serializer.errors, status_code=400, message="User not updated"
            )
        return CustomResponse.not_found(status_code=404, message="User not found")


class UserSkillsAPIView(GenericAPIView):
    permission_classes = (UserIsAuthenticated,)
    serializer_class = UserSkillsSerializer

    def post(self, request: Request):
        """to add a skill to a user"""
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            skill_name = serializer.validated_data.get("name")
            if Validator.validate_string(skill_name):
                skill, created = get_or_create_skill_by_name(skill_name)
                response = {"status_code": 201, "message": "skill added successfully"}
                if skill in user.skills.all():
                    user.skills.remove(skill)
                    response["status_code"] = 204
                else:
                    user.skills.add(skill)

                return CustomResponse.success(
                    data=serializer.data,
                    status_code=response["status_code"],
                    message=response["message"],
                )
            return CustomResponse.bad_request(
                message=" there cannot be special characters in the skill name"
            )
        return CustomResponse.bad_request(
            message=" data provided is corrupted", error=serializer.errors
        )
