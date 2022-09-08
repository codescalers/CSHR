from rest_framework.serializers import ModelSerializer
from server.cshr.models.compensation import Compensation


class CompensationSerializer(ModelSerializer):
    """class CompensationSerializer to serialize the user obj"""

    class Meta:
        model = Compensation
        fields = "__all__"
        read_only_fields = ("applying_user", "approval_user", "type", "status")
