from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from server.cshr.models.compensation import Compensation
from server.cshr.serializers.users import BaseUserSerializer, TeamSerializer


class CompensationSerializer(ModelSerializer):
    """class CompensationSerializer to serialize the user obj"""
    applying_user = SerializerMethodField()
    approval_user = SerializerMethodField()
    status = SerializerMethodField()
    type = SerializerMethodField()
    created_at = SerializerMethodField()

    class Meta:
        model = Compensation
        fields = [
            "applying_user",
            "approval_user",
            "from_date",
            "end_date",
            "reason",
            "status",
            "type",
            "created_at",
            "id"
        ]
    
    def get_applying_user(self, obj: Compensation) -> TeamSerializer:
        """Return an obj of user"""
        return TeamSerializer(obj.applying_user).data
    
    def get_status(self, obj: Compensation) -> str:
        """Return the actual string of status"""
        return obj.status
    
    def get_type(self, obj: Compensation) -> str:
        """Return the actual string of type"""
        return obj.type

    def get_created_at(self, obj: Compensation) -> str:
        """Return the actual string of created_at"""
        return obj.created_at
    
    def get_approval_user(self, obj: Compensation) -> TeamSerializer:
        """Return an obj of user"""
        return TeamSerializer(obj.approval_user).data if obj.approval_user is not None else None


class CompensationUpdateSerializer(ModelSerializer):
    class Meta:
        model = Compensation
        exclude = ("approval_user",)


class LandingPageCompensationSerializer(ModelSerializer):
    """Implemented to return just custom compensation fields to landing page endpoint."""

    applying_user = SerializerMethodField()
    approval_user = SerializerMethodField()

    class Meta:
        model = Compensation
        fields = [
            "id",
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
