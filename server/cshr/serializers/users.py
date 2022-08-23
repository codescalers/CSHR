from urllib.request import Request
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.cshr.models.company_properties import Company_properties
from server.cshr.models.users import User
from ..models.requests import Requests
from ..models.training_courses import Training_Courses
from ..serializers.skills import SkillsSerializer
from ..serializers.training_courses import TrainingCoursesSerializer
 



class GeneralUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user
    """
    user_location = SerializerMethodField()
    user_skills = SerializerMethodField()
    user_certificates = SerializerMethodField()

 

    class Meta:
        model = User
        fields = [
            "email", "full_name", "image", "telegram_link",
            "birthday", "user_location", "user_skills" , "user_certificates" ,"reporting_to","created_at"
        ]

    def get_user_location(self, obj):
        location = obj.location
        return location.name

    def get_user_skills(self, obj):
        skills = obj.skills
        return SkillsSerializer(skills, many=True).data

    def get_user_certificates(self,obj):
        training_courses= Training_Courses.objects.filter(user = obj.id)
        
        return TrainingCoursesSerializer(training_courses, many=True).data

class SupervisorUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user to a supervisor
    """
    user_location = SerializerMethodField()
    user_skills = SerializerMethodField()
    user_certificates = SerializerMethodField()
    user_properties = SerializerMethodField()
 

    class Meta:
        model = User
        fields = [
            "email", "full_name", "image", "telegram_link",
            "birthday", "user_location", "user_skills" ,
             "user_certificates" ,"reporting_to","created_at","social_insurance_number", "team"
        ]

    def get_user_location(self, obj):
        location = obj.location
        return location.name

    def get_user_skills(self, obj):
        skills = obj.skills
        return SkillsSerializer(skills, many=True).data

    def get_user_certificates(self,obj):
        training_courses= Training_Courses.objects.filter(user = obj.id)
        
        return TrainingCoursesSerializer(training_courses, many=True).data
    def get_user_properties(self,obj):
        company_properties= Company_properties.objects.filter(user= obj.id)
        return 
    

  
