from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.cshr.models.training_courses import Training_Courses


class TrainingCoursesSerializer(ModelSerializer):
    """
    This class will be used to get all info about a training course
    """

    user = SerializerMethodField(read_only=True)

    class Meta:
        model = Training_Courses
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.id
