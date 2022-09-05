from rest_framework.serializers import ModelSerializer
from server.cshr.models.compensation import Compensation


class CompensationSerializer(ModelSerializer):
    """class CompensationSerializer to serialize the user obj"""

    class Meta:
        model = Compensation
        fields = ["reason", "from_date", "end_date"]