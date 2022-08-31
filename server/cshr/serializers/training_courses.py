from rest_framework.serializers import ModelSerializer, SerializerMethodField

from server.cshr.models.training_courses import TrauningCourses


class TrainingCoursesSerializer(ModelSerializer):
    """
    This class will be used to get all info about a training course
    """

    user = SerializerMethodField(read_only=True)

    class Meta:
        model = TrauningCourses
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.id
