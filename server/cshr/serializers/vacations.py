"""This file will containes all vacation serializers."""
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from server.cshr.models.vacations import Vacation
from server.cshr.serializers.users import BaseUserSerializer


class VacationsSerializer(ModelSerializer):
    class Meta:
        model = Vacation
        fields = "__all__"
        read_only_fields = ("applying_user", "approval_user", "type", "status")


class VacationsUpdateSerializer(ModelSerializer):
    class Meta:
        model = Vacation
        exclude = ("approval_user",)


class LandingPageVacationsSerializer(ModelSerializer):
    """Implemented to return just custom vacation fields to landing page endpoint."""

    applying_user = SerializerMethodField()
    approval_user = SerializerMethodField()

    class Meta:
        model = Vacation
        fields = [
            "reason",
            "from_date",
            "end_date",
            "status",
            "applying_user",
            "approval_user",
        ]

    def get_applying_user(self, obj: Vacation) -> BaseUserSerializer:
        return BaseUserSerializer(obj.applying_user).data

    def get_approval_user(self, obj: Vacation) -> BaseUserSerializer:
        return BaseUserSerializer(obj.approval_user).data
