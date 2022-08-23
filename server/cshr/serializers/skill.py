from rest_framework.serializers import ModelSerializer
from server.cshr.models.skills import Skills


class SkillSerializer(ModelSerializer):
    """
    This class will be used to get all info about a skill
    """

    class Meta:
        model = Skills
        fields = ["name"]
