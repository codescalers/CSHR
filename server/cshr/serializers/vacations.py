from rest_framework.serializers import ModelSerializer
from server.cshr.models.vacations import Vacation


class VacationsSerializer(ModelSerializer):
    class Meta:
        model = Vacation
        fields = "__all__"
        read_only_fields = ("applying_user", "approval_user", "type", "status")


class VacationsUpdateSerializer(ModelSerializer):
    class Meta:
        model = Vacation
        exclude = ("approval_user",)
