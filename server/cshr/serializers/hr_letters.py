from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from server.cshr.models.hr_letters import HrLetters, UserDocements
from server.cshr.serializers.users import BaseUserSerializer


class HrLetterSerializer(ModelSerializer):
    class Meta:
        model = HrLetters
        fields = "__all__"
        read_only_fields = ("applying_user", "approval_user", "type", "status")


class HrLetterUpdateSerializer(ModelSerializer):
    class Meta:
        model = HrLetters
        exclude = ("approval_user",)


class LandingPageHrLetterSerializer(ModelSerializer):
    """Implemented to return just custom Hr Letters fields to landing page endpoint."""

    applying_user = SerializerMethodField()
    approval_user = SerializerMethodField()

    class Meta:
        model = HrLetters
        fields = [
            "id",
            "addresses",
            "status",
            "applying_user",
            "approval_user",
            "with_date",
            "date",
            "created_at",
        ]

    def get_applying_user(self, obj: HrLetters) -> BaseUserSerializer:
        """
        this function return request's applying user
        """
        return BaseUserSerializer(obj.applying_user).data

    def get_approval_user(self, obj: HrLetters) -> BaseUserSerializer:
        """
        this function return request's approval user
        """
        return BaseUserSerializer(obj.approval_user).data


class UserDocementsSerializer(ModelSerializer):
    class Meta:
        model = UserDocements
        fields = "__all__"
