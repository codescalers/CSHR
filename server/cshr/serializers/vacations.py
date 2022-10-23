"""This file will containes all vacation serializers."""
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from server.cshr.models.users import User
from server.cshr.models.vacations import Vacation, VacationBalance
from server.cshr.serializers.users import BaseUserSerializer, TeamSerializer
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
            "change_log",
            "type",
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


class VacationBalanceSerializer(ModelSerializer):
    """Class user balance to update user balance."""

    user = SerializerMethodField()

    class Meta:
        model = VacationBalance
        fields = [
            "user",
            "sick_leaves",
            "compensation",
            "unpaid",
            "annual_leaves",
            "emergency_leaves",
            "leave_excuses",
            "public_holidays",
        ]

    def get_user(self, obj: User):
        """This method to return user data instead of his id"""
        return TeamSerializer(obj.user).data


class UserBalanceUpdateSerializer(serializers.Serializer):
    ids = serializers.JSONField(default=list)
    type = serializers.CharField()
    new_value = serializers.IntegerField()
