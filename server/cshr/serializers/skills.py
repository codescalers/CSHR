from rest_framework.serializers import ModelSerializer


from ..models.skills import Skills


class SkillsSerializer(ModelSerializer):
    """
    This class will be used to get all info about a training course
    """

    class Meta:
        model = Skills
        fields = "__all__"
