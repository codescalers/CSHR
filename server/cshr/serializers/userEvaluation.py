from rest_framework.serializers import ModelSerializer
from cshr.models.evaluations import UserEvaluations


class UserEvaluationSerializer(ModelSerializer):
    """
    This class will be used to get all info about an evaluation
    """

    class Meta:
        model = UserEvaluations
        fields = ["user", "quarter", "link", "score"]
