import re
from typing import Any
from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.request import Request

class UserIsAuthenticated(permissions.BasePermission):
    '''
    logged in permission
    '''

    def has_permission(self, request: Request) -> bool:
        if request.user.is_authenticated():
            return True
        raise PermissionDenied

class IsAdmin(permissions.BasePermission):
    '''
    admin permission
    '''
    def has_permission(self, request: Request) -> bool:
        if request.user.is_authenticated():
            

