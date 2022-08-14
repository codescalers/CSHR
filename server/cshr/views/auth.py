from django.contrib.auth.hashers import make_password
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegisterAPIView(GenericAPIView):
    """Class RegisterAPIView to register a new user into database"""
    serializer_class = RegisterSerializer
    def post(self, request: Request) -> Response:
        """Method to register a new user"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data = serializer.data,
                message = "User created successfully",
                status_code=201
            )
        return CustomResponse.bad_request(
            error = serializer.errors,
            message = "User creation failed"
        )