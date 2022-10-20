from typing import List
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.users import User
from server.cshr.api.permission import (
    IsAdmin,
    IsSupervisor,
    IsUser,
    UserIsAuthenticated,
)
from server.cshr.utils.validations import Validator
from server.cshr.api.response import CustomResponse
from server.cshr.serializers.users import (
    GeneralUserSerializer,
    SupervisorUserSerializer,
    AdminUserSerializer,
    SelfUserSerializer,
    UpdateUserSerializer,
    UserSkillsSerializer,
)
from server.cshr.services.users import (
    get_user_by_id,
    get_or_create_skill_by_name,
    get_all_of_users,
    get_user_team_leads,
    get_user_team_members,
)
from server.cshr.serializers.users import TeamSerializer


class BaseGeneralUserAPIView(ListAPIView, GenericAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = GeneralUserSerializer

    def get_queryset(self) -> Response:
        """get all users in the system for a normal user"""
        query_set = get_all_of_users()
        return query_set


class TeamAPIView(ListAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = TeamSerializer

    def get_queryset(self) -> Response:
        """
        Get all team information, Team leaders and team members
        """
        user: User = self.request.user
        query_set: List[User] = get_user_team_members(user)
        return query_set


class SupervisorsAPIView(ListAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = TeamSerializer

    def get_queryset(self) -> Response:
        """
        Get all team information, Team leaders and team members
        """
        user: User = self.request.user
        query_set: List[User] = get_user_team_leads(user)
        return query_set


class GeneralUserAPIView(ListAPIView, GenericAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = GeneralUserSerializer

    def get(self, request: Request, id: str) -> Response:
        """To get a user by id"""
        user = get_user_by_id(id)
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200,
            )
        return CustomResponse.not_found(message="User not found", status_code=404)


class BaseSupervisorUserAPIView(ListAPIView, GenericAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = SupervisorUserSerializer

    def get_queryset(self) -> Response:
        """get all users in the system for a supervisor"""
        query_set = get_all_of_users()
        return query_set


class SupervisorUserAPIView(ListAPIView, GenericAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = SupervisorUserSerializer

    def get(self, request: Request, id: str) -> Response:
        """To get a user by id"""
        user = get_user_by_id(id)
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200,
            )
        return CustomResponse.not_found(message="User not found", status_code=404)


class BaseAdminUserAPIView(ListAPIView, GenericAPIView):
    """
    admin have full control over a user account
    """

    permission_classes = [IsAdmin]
    serializer_class = AdminUserSerializer

    def get_queryset(self) -> Response:
        """get all users in the system for an admin"""
        query_set = get_all_of_users()
        return query_set


class AdminUserAPIView(ListAPIView, GenericAPIView):
    """
    admin have full control over a user account
    """

    permission_classes = [IsAdmin]
    serializer_class = AdminUserSerializer

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

    def get(self, request: Request, id: str) -> Response:
        """To get a user by id"""
        user = get_user_by_id(id)
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200,
            )
        return CustomResponse.not_found(message="User not found", status_code=404)


class SelfUserAPIView(ListAPIView, GenericAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = SelfUserSerializer

    def get(self, request: Request) -> Response:
        """To get a user by id"""
        user = self.request.user
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200,
            )
        return CustomResponse.not_found(message="User not found", status_code=404)

class UpdateUserProfileUserAPIView(GenericAPIView):
    permission_classes = [IsUser | IsAdmin]
    serializer_class = UpdateUserSerializer

    def put(self, request: Request, id: str, format=None) -> Response:
        """To update a user"""
        user = get_user_by_id(id)
        if user is None:
            return CustomResponse.not_found(status_code=404, message="User not found")
        remove_image: bool = request.data.get("remove_image")
        if request.data.get("image") == "":
            request.data["image"] = user.image if user.image else None

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if remove_image:
                user.image.delete()
                user.save()
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="User updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, status_code=400, message="User not updated"
        )


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
