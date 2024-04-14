"""This file will containes all vacation serializers."""
from rest_framework.serializers import (
    ModelSerializer,
    DateTimeField,
    SerializerMethodField,
)
from cshr.models.users import User
from cshr.models.vacations import (
    OfficeVacationBalance,
    PublicHoliday,
    Vacation,
    VacationBalance,
)
from cshr.serializers.office import OfficeSerializer
from cshr.serializers.users import BaseUserSerializer, TeamSerializer
from rest_framework import serializers


class VacationsSerializer(ModelSerializer):
    class Meta:
        model = Vacation
        fields = ["id", "reason", "from_date", "end_date", "applying_user", "approval_user", "type", "status", "created_at" ]
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


class CustomDateField(serializers.ReadOnlyField):
    """
    Custom read-only field to serialize datetime as date.
    """
    def to_representation(self, value):
        return value.date() if value else None


class LandingPageVacationsSerializer(ModelSerializer):
    """Implemented to return just custom vacation fields to landing page endpoint."""

    applying_user = SerializerMethodField()
    approval_user = SerializerMethodField()
    
    from_date = CustomDateField()  # Convert datetime to date
    end_date = CustomDateField()   # Convert datetime to date


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


class GetOfficeVacationBalanceSerializer(ModelSerializer):
    public_holidays = SerializerMethodField()
    location = SerializerMethodField()

    class Meta:
        model = OfficeVacationBalance
        fields = [
            "annual_leaves",
            "compensation",
            "emergency_leaves",
            "leave_excuses",
            "year",
            "public_holidays",
            "location",
        ]

    def get_location(self, obj: OfficeVacationBalance):
        return OfficeSerializer(obj.location).data

    def get_public_holidays(self, obj: OfficeVacationBalance):
        return PublicHoliday.objects.filter(
            id__in=obj.public_holidays.all()
        ).values_list("holiday_date", flat=True)


class PostOfficeVacationBalanceSerializer(ModelSerializer):
    public_holidays = serializers.JSONField(default=list)

    class Meta:
        model = OfficeVacationBalance
        fields = [
            "annual_leaves",
            "compensation",
            "emergency_leaves",
            "leave_excuses",
            "year",
            "public_holidays",
        ]


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


class UserBalanceVlaueSerializer(serializers.Serializer):
    reserved = serializers.IntegerField()
    all = serializers.IntegerField()


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
        value = {
            "reserved": obj.sick_leaves,
            "all": obj.office_vacation_balance.sick_leaves,
        }
        return UserBalanceVlaueSerializer(value).data

    def get_compensation(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        value = {
            "reserved": obj.compensation,
            "all": obj.office_vacation_balance.compensation,
        }
        return UserBalanceVlaueSerializer(value).data

    def get_unpaid(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        value = {
            "reserved": obj.unpaid,
            "all": obj.office_vacation_balance.unpaid,
        }
        return UserBalanceVlaueSerializer(value).data

    def get_annual_leaves(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        value = {
            "reserved": obj.annual_leaves,
            "all": obj.office_vacation_balance.annual_leaves,
        }
        return UserBalanceVlaueSerializer(value).data

    def get_emergency_leaves(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        value = {
            "reserved": obj.emergency_leaves,
            "all": obj.office_vacation_balance.emergency_leaves,
        }
        return UserBalanceVlaueSerializer(value).data

    def get_leave_excuses(self, obj: VacationBalance):
        """This method returns the actual user balance values."""
        value = {
            "reserved": obj.leave_excuses,
            "all": obj.office_vacation_balance.leave_excuses,
        }
        return UserBalanceVlaueSerializer(value).data


class VacationBalanceAdjustmentSerializer(serializers.Serializer):
    officeId = serializers.IntegerField()
    value = serializers.IntegerField()
    reason = serializers.CharField()

class AdminApplyVacationForUserSerializer(serializers.Serializer):
    reason = serializers.CharField()
    from_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
