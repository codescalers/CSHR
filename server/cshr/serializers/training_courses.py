from rest_framework.serializers import ModelSerializer, SerializerMethodField
 
from ..models.requests import Requests
from ..models.training_courses import Training_Courses
 
from django.conf import settings
import os



class TrainingCoursesSerializer(ModelSerializer):
    """
    This class will be used to get all info about a training course
    """
    class Meta:
        model = Training_Courses
        fields = ["name","certificate_link"]