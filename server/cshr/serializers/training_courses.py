from rest_framework.serializers import ModelSerializer, SerializerMethodField

from cshr.models.training_courses import TrainingCourses


class TrainingCoursesSerializer(ModelSerializer):
    """
    This class will be used to get all info about a training course
    """

    user = SerializerMethodField(read_only=True)

    class Meta:
        model = TrainingCourses
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.id
