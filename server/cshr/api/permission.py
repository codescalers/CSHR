from rest_framework import permissions
from rest_framework.request import Request
from server.cshr.services.users import get_user_type_by_id
from server.cshr.models.users import USER_TYPE
from rest_framework.views import APIView
from server.cshr.models.users import User


class UserIsAuthenticated(permissions.BasePermission):
    """
    logged in permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated and request.user.is_active:
            return True
        return False


class IsAdmin(permissions.BasePermission):
    """
    admin permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            userType = get_user_type_by_id(request.user.id)
            return userType == USER_TYPE.ADMIN
        return False


class IsSupervisor(permissions.BasePermission):
    """
    supervisor permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            userType = get_user_type_by_id(request.user.id)
            return userType == USER_TYPE.SUPERVISOR
        return False


class IsUser(permissions.BasePermission):
    """
    normal user permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            userType = get_user_type_by_id(request.user.id)
            return userType == USER_TYPE.USER
        return False


class CustomPermissions:
    """for check the type of user in views"""

    @staticmethod
    def admin_or_supervisor(user: User) -> bool:
        """return True only if the user is a supervisor or admin"""
        return user.user_type in [USER_TYPE.ADMIN, USER_TYPE.SUPERVISOR]

    @staticmethod
    def admin(user: User) -> bool:
        """return True only if the user is an admin"""
        return user.user_type == USER_TYPE.ADMIN
