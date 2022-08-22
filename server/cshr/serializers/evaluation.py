from rest_framework.serializers import ModelSerializer
from server.cshr.models.evaluations import Evaluations

class EvaluationSerializer(ModelSerializer):
    """
    This class will be used to get all info about an evaluation
    """

    class Meta:
        model = Evaluations
        fields = ["user", "link"]
