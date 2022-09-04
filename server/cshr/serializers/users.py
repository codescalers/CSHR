"""This file will containes all user serializers."""
from rest_framework.serializers import ModelSerializer
from server.cshr.models.users import User


class BaseUserSerializer(ModelSerializer):
    """Implemented to be standered class for multiple usecases."""

    class Meta:
        model = User
        fields = ["full_name", "email", "image"]
