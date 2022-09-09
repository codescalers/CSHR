from rest_framework.serializers import ModelSerializer
from server.cshr.models.evaluations import UserEvaluations, Evaluations


class EvaluationSerializer(ModelSerializer):
    """
    This class will be used to get all info about an evaluation
    """

    class Meta:
        model = Evaluations
        fields = ["form", "quarter", "link"]


class UserEvaluationSerializer(ModelSerializer):
    """
    This class will be used to get all info about user evaluation
    """

    class Meta:
        model = UserEvaluations
        fields = ["user", "quarter", "link", "score"]
