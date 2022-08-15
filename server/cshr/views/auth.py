from django.contrib.auth.hashers import make_password
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from server.cshr.serializers.auth import (
    RegisterSerializer,
    UpdateUserSettingsSerializer,
    MyTokenObtainPairSerializer,
    MyTokenRefreshSerializer,
)
from server.cshr.services.users import get_user_by_id


class RegisterAPIView(GenericAPIView):
    """Class RegisterAPIView to register a new user into database"""

    serializer_class = RegisterSerializer

    def post(self, request: Request) -> Response:
        """Method to register a new user"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return CustomResponse.success(
            #     data = serializer.data,
            #     message = "User created successfully",
            #     status_code=201
            # )
        # return CustomResponse.bad_request(
        #     error = serializer.errors,
        #     message = "User creation failed"
        # )


class LoginByTokenAPIView(TokenObtainPairView):
    """Class LoginByTokenAPIView to login a user by jwt token"""

    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    """
    An end point to refresh the user token
    """

    serializer_class = MyTokenRefreshSerializer


class UpdateUserSettingsAPIView(GenericAPIView):
    """This class to update profile info"""

    serializer_class = UpdateUserSettingsSerializer
    # permission_classes = (UserIsAuthenticated,)

    def put(self, request: Request) -> Response:
        """Update user settings"""
        user = get_user_by_id(request.user.id)
        serializer = self.get_serializer(user, data=request.data)
        if not request.data.get("password"):
            request.data["password"] = user.password
        else:
            request.data["password"] = make_password(request.data["password"])

        print(request.data)
        if serializer.is_valid():
            serializer.save()
            # return CustomResponse.success(
            #     data=serializer.data,
            #     message="Profile updated successfully.",
            #     status_code=201
            # )
        # return CustomResponse.bad_request(
        #     error=serializer.errors,
        #     message="Profile update failed.",

    # )
