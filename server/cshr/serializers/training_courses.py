from rest_framework.serializers import ModelSerializer, SerializerMethodField
 
from ..models.requests import Requests
from ..models.training_courses import Training_Courses
 
from django.conf import settings
import os



class TrainingCoursesSerializer(ModelSerializer):
    """
    This class will be used to get all info about a training course
    """
    user = SerializerMethodField(read_only= True)
    class Meta:
        model = Training_Courses
        fields = "__all__"
    def get_user(self, obj):
        return obj.user.id