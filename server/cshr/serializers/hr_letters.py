
from rest_framework.serializers import ModelSerializer
from server.cshr.models.hr_letters import HrLetters


class HrLetterSerializer(ModelSerializer):
    class Meta:
        model = HrLetters
        fields = "__all__"
        read_only_fields = ("applying_user", "approval_user", "type", "status")


class HrLetterUpdateSerializer(ModelSerializer):
    class Meta:
        model = HrLetters
        exclude = ("approval_user",)