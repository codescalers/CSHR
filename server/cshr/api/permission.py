from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.request import Request
from server.cshr.services.users import get_user_type_by_id

from rest_framework.views import APIView


class UserIsAuthenticated(permissions.BasePermission):
    """
    logged in permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            return True
        raise PermissionDenied


class IsAdmin(permissions.BasePermission):
    """
    admin permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            userType = get_user_type_by_id(request.user.id)
            if userType == "Admin":
                return True
            raise PermissionDenied
        raise PermissionDenied


class IsSupervisor(permissions.BasePermission):
    """
    supervisor permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            userType = get_user_type_by_id(request.user.id)
            if userType == "Supervisor":
                return True
            raise PermissionDenied
        raise PermissionDenied


class IsUser(permissions.BasePermission):
    """
    normal user permission
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            userType = get_user_type_by_id(request.user.id)
            if userType == "Supervisor":
                return True
            raise PermissionDenied
        raise PermissionDenied
