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

    # user = SerializerMethodField()

    class Meta:
        model = UserEvaluations
        fields = "__all__"

    # def get_user(self, obj):
    #     return BasicUserSerializer(obj).data
