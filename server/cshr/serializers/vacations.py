from rest_framework.serializers import ModelSerializer
from server.cshr.models.vacations import Vacation


class vacations_serializer(ModelSerializer):
    class Meta:
        model = Vacation
        fields = "__all__"
        read_only_fields = ("applying_user", "approval_user", "type", "status")


class vacations_update_serializer(ModelSerializer):
    class Meta:
        model = Vacation
        exclude = ("approval_user",)
