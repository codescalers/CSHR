"""This file will containes all user serializers."""
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    DateTimeField,
    JSONField,
)
from server.cshr.models.users import User, UserSkills
from server.cshr.serializers.training_courses import TrainingCoursesSerializer
from server.cshr.serializers.company_properties import CompanyPropertiesSerializer
from server.cshr.services.training_courses import get_training_courses_for_a_user
from server.cshr.services.company_properties import (
    get_all_company_properties_for_a_user,
)
from server.cshr.services.evaluations import get_evaluations_for_a_user
from server.cshr.serializers.userEvaluation import UserEvaluationSerializer


class UserSkillsSerializer(ModelSerializer):
    """
    This class will be used to get all info about a skills
    """

    class Meta:
        model = UserSkills
        fields = [
            "name",
        ]


class GeneralUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user
    """

    user_certificates = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "image",
            "telegram_link",
            "birthday",
            "location",
            "skills",
            "user_certificates",
            "reporting_to",
            "created_at",
        ]

    def get_user_certificates(self, obj):
        training_courses = get_training_courses_for_a_user(obj.id)
        return TrainingCoursesSerializer(training_courses, many=True).data


class SupervisorUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user to a supervisor
    """

    user_certificates = SerializerMethodField()
    user_company_properties = SerializerMethodField()
    user_evaluation = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "image",
            "telegram_link",
            "birthday",
            "location",
            "skills",
            "user_certificates",
            "reporting_to",
            "created_at",
            "social_insurance_number",
            "team",
            "user_company_properties",
            "mobile_number",
            "user_evaluation",
        ]

    def get_user_certificates(self, obj):
        training_courses = get_training_courses_for_a_user(obj.id)
        return TrainingCoursesSerializer(training_courses, many=True).data

    def get_user_company_properties(self, obj):
        company_properties = get_all_company_properties_for_a_user(obj.id)
        return CompanyPropertiesSerializer(company_properties, many=True).data

    def get_user_evaluation(self, obj):
        evaluations = get_evaluations_for_a_user(obj.id)
        return UserEvaluationSerializer(evaluations, many=True).data


class AdminUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user to an admin
    """

    user_certificates = SerializerMethodField()
    user_company_properties = SerializerMethodField()
    user_evaluation = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "image",
            "telegram_link",
            "birthday",
            "location",
            "skills",
            "user_certificates",
            "reporting_to",
            "created_at",
            "social_insurance_number",
            "team",
            "user_company_properties",
            "salary",
            "mobile_number",
            "user_evaluation",
        ]

    def get_user_certificates(self, obj):
        training_courses = get_training_courses_for_a_user(obj.id)
        return TrainingCoursesSerializer(training_courses, many=True).data

    def get_user_company_properties(self, obj):
        company_properties = get_all_company_properties_for_a_user(obj.id)
        return CompanyPropertiesSerializer(company_properties, many=True).data

    def get_user_evaluation(self, obj):
        evaluations = get_evaluations_for_a_user(obj.id)
        return UserEvaluationSerializer(evaluations, many=True).data


class SelfUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user to themselves
    """

    user_certificates = SerializerMethodField()
    user_company_properties = SerializerMethodField(read_only=True)
    user_evaluation = SerializerMethodField(read_only=True)
    reporting_to = SerializerMethodField(read_only=True)
    created_at = DateTimeField(read_only=True)
    team = CharField(read_only=True)
    salary = JSONField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "image",
            "telegram_link",
            "birthday",
            "location",
            "skills",
            "user_certificates",
            "reporting_to",
            "created_at",
            "social_insurance_number",
            "team",
            "user_company_properties",
            "salary",
            "mobile_number",
            "user_evaluation",
        ]

    def get_user_certificates(self, obj):
        training_courses = get_training_courses_for_a_user(obj.id)
        return TrainingCoursesSerializer(training_courses, many=True).data

    def get_user_company_properties(self, obj):
        company_properties = get_all_company_properties_for_a_user(obj.id)
        return CompanyPropertiesSerializer(company_properties, many=True).data

    def get_user_evaluation(self, obj):
        evaluations = get_evaluations_for_a_user(obj.id)
        return UserEvaluationSerializer(evaluations, many=True).data

    def get_reporting_to(self, obj):
        reporting_to = obj.reporting_to
        return GeneralUserSerializer(reporting_to).data
    
class BaseUserSerializer(ModelSerializer):
    """Implemented to be standered class for multiple usecases."""

    class Meta:
        model = User
        fields = ["full_name", "email", "image"]
