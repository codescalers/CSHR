"""This file will containes all vacation serializers."""
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from server.cshr.models.vacations import Vacation
from server.cshr.serializers.users import BaseUserSerializer
from rest_framework import serializers


class VacationsSerializer(ModelSerializer):
    class Meta:
        model = Vacation
        fields = "__all__"
        read_only_fields = ("applying_user", "approval_user", "type", "status")


class VacationsUpdateSerializer(ModelSerializer):
    class Meta:
        model = Vacation
        exclude = ("approval_user",)


class VacationsCommentsSerializer(ModelSerializer):
    "For the users to leave a comment without updating other fields"

    class Meta:
        model = Vacation
        fields = ""


class LandingPageVacationsSerializer(ModelSerializer):
    """Implemented to return just custom vacation fields to landing page endpoint."""

    applying_user = SerializerMethodField()
    approval_user = SerializerMethodField()

    class Meta:
        model = Vacation
        fields = [
            "id",
            "reason",
            "from_date",
            "end_date",
            "status",
            "applying_user",
            "approval_user",
        ]

    def get_applying_user(self, obj: Vacation) -> BaseUserSerializer:
        """
        this function return request's applying user
        """
        return BaseUserSerializer(obj.applying_user).data

    def get_approval_user(self, obj: Vacation) -> BaseUserSerializer:
        """
        this function return request's approving user
        """
        return BaseUserSerializer(obj.approval_user).data


class UserVacationBalanceSerializer(serializers.Serializer):
    sick_leaves = serializers.FloatField()
    compensation = serializers.FloatField()
    unpaid = serializers.FloatField()
    annual_leaves = serializers.FloatField()
    emergency_leaves = serializers.FloatField()
    leave_execuses = serializers.FloatField()
    public_holidays = serializers.JSONField(default=list)
    year = serializers.IntegerField()


class UserBalanceUpdateSerializer(serializers.Serializer):
    ids = serializers.JSONField(default=list)
    type = serializers.CharField()
    new_value = serializers.IntegerField()
