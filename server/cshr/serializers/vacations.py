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


class AdminVacationBalanceSerializer(serializers.Serializer):
    sick_leaves = serializers.FloatField()
    compensation = serializers.FloatField()
    unpaid = serializers.FloatField()
    annual_leaves = serializers.FloatField()
    emergency_leaves = serializers.FloatField()
    leave_excuses = serializers.FloatField()
    public_holidays = serializers.JSONField(default=list)


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
        ]

    def get_user(self, obj: User):
        """This method to return user data instead of his id"""
        return TeamSerializer(obj.user).data


class UserBalanceUpdateSerializer(serializers.Serializer):
    ids = serializers.JSONField(default=list)
    type = serializers.CharField()
    new_value = serializers.IntegerField()


class CalculateCurrentBalanceSerializer(serializers.Serializer):
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
        ]

    def get_user(self, obj: User):
        """This method to return user data instead of his id"""
        return TeamSerializer(obj.user).data

class CalculateBalanceSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    sick_leaves = serializers.SerializerMethodField()
    compensation = serializers.SerializerMethodField()
    unpaid = serializers.SerializerMethodField()
    annual_leaves = serializers.SerializerMethodField()
    emergency_leaves = serializers.SerializerMethodField()
    leave_excuses = serializers.SerializerMethodField()

    class Meta:
        model = VacationBalance
        fields = [
            "sick_leaves",
            "compensation",
            "unpaid",
            "annual_leaves",
            "emergency_leaves",
            "leave_excuses",
        ]

    def get_user(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        return TeamSerializer(obj.user).data

    def get_sick_leaves(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        return [obj.sick_leaves, obj.actual_balance.get('sick_leaves')]
    
    def get_compensation(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        return [obj.compensation, obj.actual_balance.get('compensation')]
    
    def get_unpaid(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        return [obj.unpaid, obj.actual_balance.get('unpaid')]
    
    def get_annual_leaves(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        return [obj.annual_leaves, obj.actual_balance.get('annual_leaves')]
    
    def get_emergency_leaves(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        return [obj.emergency_leaves, obj.actual_balance.get('emergency_leaves')]
    
    def get_leave_excuses(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        return [obj.leave_excuses, obj.actual_balance.get('leave_excuses')]
