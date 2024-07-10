from typing import Dict, List
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from cshr.api.permission import IsAdmin, UserIsAuthenticated
from django.contrib.auth.hashers import check_password, make_password


from cshr.serializers.auth import (
    ChangePasswordSerializer,
    RegisterSerializer,
    MyTokenObtainPairSerializer,
    MyTokenRefreshSerializer,
)
from cshr.api.response import CustomResponse
from cshr.services.users import get_or_create_user_balance, get_user_by_email
from cshr.models.vacations import REASON_CHOICES
from cshr.models.users import User


class RegisterApiView(GenericAPIView):
    """
    API view for registering a new user into the database.
    """

    serializer_class = RegisterSerializer
    permission_classes = [IsAdmin]

    def post(self, request: Request) -> Response:
        """
        Handle POST request to register a new user.

        Parameters:
        request (Request): The request object containing user data.

        Returns:
        Response: Custom response indicating success or failure.
        """
        # Handle optional image field
        if request.data.get("image") == "":
            request.data["image"] = None

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user: User = serializer.save(joining_at=request.data.get("joining_at"))
            calculate_balance: bool = request.data.get("calculate_balance")
            user_balance: Dict = request.data.get("user_balance")

            if calculate_balance:
                if not user_balance:
                    return CustomResponse.bad_request(
                        message="The `calculate_balance` option is enabled while there is no `user_balance` object sent."
                    )

                # Check for required fields in the user_balance object
                required_balance_fields: List[str] = [
                    REASON_CHOICES.ANNUAL_LEAVES,
                    REASON_CHOICES.EMERGENCY_LEAVE,
                    REASON_CHOICES.LEAVE_EXCUSES,
                ]
                for field in required_balance_fields:
                    if not user_balance.get(field):
                        return CustomResponse.bad_request(
                            message=f"The {field} is missing in the `user_balance` object."
                        )

                # Create or update user balance
                get_or_create_user_balance(user, user_balance)

            return CustomResponse.success(
                data=serializer.data,
                message="User created successfully",
                status_code=201,
            )

        # Handle invalid serializer data
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
            user_email = serializer.validated_data.get("email")
            user = get_user_by_email(user_email)
            if not user.is_active:
                return CustomResponse.unauthorized(
                    message="You don't have permission to perform this action."
                )
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
            return CustomResponse.unauthorized(
                message="Incorrect password. Please ensure that the password provided is accurate."
            )
        return CustomResponse.bad_request(
            message="Please make sure that you entered a valid data.",
            error=serializer.errors,
        )
