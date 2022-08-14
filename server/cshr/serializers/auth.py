from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.settings import api_settings
from rest_framework import exceptions
from django.contrib.auth.hashers import check_password

from server.cshr.models.users import  User

class RegisterSerializer(ModelSerializer):
    """class RegisterSerializer to serialize the user obj"""
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'email', 'password'
        )