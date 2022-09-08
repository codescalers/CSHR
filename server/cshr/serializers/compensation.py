from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from server.cshr.models.compensation import Compensation
from server.cshr.serializers.users import BaseUserSerializer


class CompensationSerializer(ModelSerializer):
    """class CompensationSerializer to serialize the user obj"""

    class Meta:
        model = Compensation
        fields = ["reason", "from_date", "end_date"]


class LandingPageCompensationSerializer(ModelSerializer):
    """Implemented to return just custom compensation fields to landing page endpoint."""

    applying_user = SerializerMethodField()
    approval_user = SerializerMethodField()

    class Meta:
        model = Compensation
        fields = [
            "reason",
            "from_date",
            "end_date",
            "status",
            "applying_user",
            "approval_user",
        ]

    def get_applying_user(self, obj: Compensation) -> BaseUserSerializer:
        """
        this function return request's applying user
        """
        return BaseUserSerializer(obj.applying_user).data

    def get_approval_user(self, obj: Compensation) -> BaseUserSerializer:
        """
        this function return request's approval user
        """
        return BaseUserSerializer(obj.approval_user).data
