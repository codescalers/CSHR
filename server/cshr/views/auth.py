from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from server.cshr.api.permission import IsAdmin, UserIsAuthenticated
from django.contrib.auth.hashers import check_password, make_password


from server.cshr.serializers.auth import (
    ChangePasswordSerializer,
    RegisterSerializer,
    MyTokenObtainPairSerializer,
    MyTokenRefreshSerializer,
)
from server.cshr.api.response import CustomResponse


class RegisterApiView(GenericAPIView):
    """Class RegisterAPIView to register a new user into database"""

    serializer_class = RegisterSerializer
    permission_classes = [IsAdmin]

    def post(self, request: Request) -> Response:
        """Method to register a new user"""
        serializer = self.get_serializer(data=request.data)
        if request.data.get("image") == "":
            request.data["image"] = None
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="User created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="User creation failed"
        )


class LoginByTokenApiView(TokenObtainPairView):
    """Class LoginByTokenAPIView to login a user by jwt token"""

    serializer_class = MyTokenObtainPairSerializer

    def post(self, request: Request) -> Response:
        """Method to register a new user"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            return CustomResponse.success(
                data=serializer.custom_token(data=serializer.data),
                message="User logged in successfully",
            )


class MyTokenRefreshView(TokenRefreshView):
    """
    An end point to refresh the user token
    """

    serializer_class = MyTokenRefreshSerializer


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [
        UserIsAuthenticated,
    ]

    def put(self, request: Request) -> Response:
        """Class change password to change user password."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_password: str = request.user.password

            new_password = make_password(serializer.validated_data.get("new_password"))
            checked_password: bool = check_password(
                serializer.validated_data.get("old_password"), user_password
            )
            if checked_password:
                request.user.password = new_password
                request.user.save()
                return CustomResponse.success(message="Success updated password")
            return CustomResponse.unauthorized()
        return CustomResponse.bad_request(
            message="Please make sure that you entered a valid data",
            error=serializer.errors,
        )
