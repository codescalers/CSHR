from rest_framework.serializers import ModelSerializer, SerializerMethodField
from cshr.models.requests import Requests
from cshr.serializers.users import BaseUserSerializer


class RequestsSerializer(ModelSerializer):
    """
    Serializer for Requests model to serialize/deserialize Requests objects.
    Fields included: type, status, id.
    """

    applying_user = SerializerMethodField()
    approval_user = SerializerMethodField()

    class Meta:
        model = Requests
        fields = [
            "type",
            "status",
            "id",
            "applying_user",
            "approval_user",
            "approval_user",
        ]

    def get_applying_user(self, obj):
        return BaseUserSerializer(obj.applying_user).data

    def get_approval_user(self, obj):
        if obj.approval_user:
            return BaseUserSerializer(obj.approval_user).data
        return None
