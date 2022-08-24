from rest_framework.serializers import ModelSerializer
from server.cshr.models.hr_letters import HR_LETTERS


class hr_letter_serializer(ModelSerializer):
    class Meta:
        model = HR_LETTERS
        fields = "__all__"
        read_only_fields = ("applying_user", "approval_user", "type", "status")


class hr_letter_update_serializer(ModelSerializer):
    class Meta:
        model = HR_LETTERS
        exclude = ("approval_user",)
