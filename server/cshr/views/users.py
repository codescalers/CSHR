from typing import List
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from cshr.models.users import User, UserSkills
from cshr.api.permission import (
    IsAdmin,
    IsSupervisor,
    UserIsAuthenticated,
)
from cshr.services.office import get_office_by_id
from cshr.utils.validations import Validator
from cshr.api.response import CustomResponse
from cshr.serializers.users import (
    ActiveUserSerializer,
    BaseUserSerializer,
    GeneralUserSerializer,
    PostUserSkillsSerializer,
    SupervisorUserSerializer,
    AdminUserSerializer,
    SelfUserSerializer,
    UpdateUserSerializer,
    UserSkillsSerializer,
)
from cshr.services.users import (
    filter_users_by_birthdates,
    get_admin_office_users,
    get_all_skills,
    get_supervisors,
    get_user_by_id,
    get_or_create_skill_by_name,
    get_all_of_users,
    get_user_team_leads,
    get_user_team_members,
)
from cshr.serializers.users import TeamSerializer


class BaseGeneralUserAPIView(ListAPIView, GenericAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = GeneralUserSerializer

    def get_queryset(self) -> Response:
        """get all users in the system for a normal user"""
        # print()
        if self.request.query_params.get("location_id"):
            location_id = self.request.query_params.get("location_id")
            options = {"location": {"id": location_id}}
            query_set = get_all_of_users(options)
        else:
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


class TeamSupervisorsAPIView(ListAPIView):
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


class GetUsersInAdminOfficeAPIView(ListAPIView, GenericAPIView):
    """
    Custom class to restrict access to admins working in the same office as the user.
    For example, in the update user balance endpoint, there is a select area in the frontend where admins can load users
    and update the balance for specific users. This permission ensures that only users working in the same office as the admin
    are displayed for selection.
    """

    permission_classes = [IsAdmin]
    serializer_class = GeneralUserSerializer

    def get_queryset(self) -> Response:
        """get all users in the system for a normal user"""
        query_set = get_admin_office_users(self.request.user)
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


class SetActiveUserAPIView(GenericAPIView):
    """Class to set the user as an active user."""

    serializer_class = ActiveUserSerializer
    permission_classes = [
        IsAdmin,
    ]

    def put(self, request: Request) -> Response:
        """Set user as an active user."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get("user_id")
            user = get_user_by_id(user_id)
            if not user:
                return CustomResponse.not_found("User not found.")
            user.is_active = True
            user.save()
            return CustomResponse.success(
                data=serializer.data, message="User noe active user"
            )
        return CustomResponse.bad_request(
            message="Failed to set the user as an active user, Please make sure that you entered valid data.",
            error=serializer.errors,
        )


class SetInActiveUserAPIView(GenericAPIView):
    """Class to set the user as an inactive user."""

    serializer_class = ActiveUserSerializer
    permission_classes = [
        IsAdmin,
    ]

    def put(self, request: Request) -> Response:
        """Set user as an inactive user."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get("user_id")
            user = get_user_by_id(user_id)
            if not user:
                return CustomResponse.not_found("User not found.")
            user.is_active = False
            user.save()
            return CustomResponse.success(
                data=serializer.data, message="User now inactive user"
            )
        return CustomResponse.bad_request(
            message="Failed to set the user as an inactive user, Please make sure that you entered valid data.",
            error=serializer.errors,
        )


class UpdateUserProfileUserAPIView(GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UpdateUserSerializer

    def put(self, request: Request, id: str, format=None) -> Response:
        """To update a user"""
        user = get_user_by_id(id)
        if user is None:
            return CustomResponse.not_found(status_code=404, message="User not found")

        image = request.data.get("image")

        if not image:
            request.data["image"] = user.image if user.image else None

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            office = get_office_by_id(request.data.get("location"))
            user: User = serializer.save(
                team=request.data.get("team"),
                gender=request.data.get("gender"),
                location=office,
                joining_at=request.data.get("joining_at"),
                reporting_to=request.data.get("reporting_to"),
            )

            return CustomResponse.success(
                data=serializer.data, status_code=202, message="User updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, status_code=400, message="User not updated"
        )


class UserSkillsAPIView(GenericAPIView):
    permission_classes = (UserIsAuthenticated,)
    serializer_class = UserSkillsSerializer

    def get(self, request: Request):
        skills: UserSkills = get_all_skills()
        serializer: UserSkillsSerializer = self.get_serializer(skills, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Success found skills"
        )


class PostUserSkillsAPIView(GenericAPIView):
    serializer_class = PostUserSkillsSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request):
        """to add a skill to a user"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id: int = request.data.get("user_id")
            user: User = get_user_by_id(user_id)
            skills = serializer.validated_data.get("skills")
            if type(skills) is not list:
                skills = [skills]

            for skill in skills:
                if Validator.validate_string(skill):
                    skill_, created = get_or_create_skill_by_name(skill)
                    user.skills.add(skill_)
                else:
                    return CustomResponse.bad_request(
                        message=" there cannot be special characters in the skill name"
                    )
            return CustomResponse.success(
                data=serializer.data,
                message="Skills added successfully",
            )
        return CustomResponse.bad_request(
            message=" data provided is corrupted", error=serializer.errors
        )


class GetUsersBirthDatesAPIView(GenericAPIView):
    """Class to filter all users birthdates based on requested day."""

    serializer_class = BaseUserSerializer
    permission_classes = [
        UserIsAuthenticated,
    ]

    def get(self, request: Request) -> Response:
        """Get all users birthdates based on requested day that sent as a query param"""
        if not request.query_params.get("day") or not request.query_params.get("month"):
            return CustomResponse.bad_request(
                message="You must send [day, month] to filter based on it."
            )
        month: int = int(request.query_params.get("month"))
        day: int = int(request.query_params.get("day"))
        users: List[User] = filter_users_by_birthdates(month, day)
        serializer = self.serializer_class(users, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Users founded successfully."
        )

class SupervisorsAPIView(ListAPIView, GenericAPIView):
    """method to get all Company properties"""

    serializer_class = GeneralUserSerializer
    permission_class = [IsAdmin | IsSupervisor]

    def get_queryset(self) -> Response:
        query_set = get_supervisors()
        return query_set
