"""This file will containes all user serializers."""
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    DateField,
    JSONField,
    ListField,
    Serializer,
    IntegerField,
)
from cshr.models.users import User, UserSkills
from cshr.serializers.Image_upload import Base64ImageField
from cshr.serializers.training_courses import TrainingCoursesSerializer
from cshr.serializers.company_properties import CompanyPropertiesSerializer
from cshr.services.training_courses import get_training_courses_for_a_user
from cshr.services.company_properties import (
    get_all_company_properties_for_a_user,
)
from cshr.services.evaluations import get_evaluations_for_a_user
from cshr.serializers.userEvaluation import UserEvaluationSerializer
from cshr.serializers.office import OfficeSerializer


class ActiveUserSerializer(Serializer):
    """This class is used for setting user as an active/inactive user."""

    user_id = IntegerField()


class UserSkillsSerializer(ModelSerializer):
    """
    This class will be used to get all info about a skills
    """

    class Meta:
        model = UserSkills
        fields = [
            "name",
        ]


class PostUserSkillsSerializer(ModelSerializer):
    """
    This class will be used to get all info about a skills
    """

    skills = ListField(child=CharField())

    class Meta:
        model = UserSkills
        fields = [
            "skills",
        ]


class GeneralUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user
    """

    user_certificates = SerializerMethodField()
    image = SerializerMethodField()
    skills = SerializerMethodField()
    reporting_to = SerializerMethodField()
    location = SerializerMethodField()
    reporting_to = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "gender",
            "team",
            "image",
            "telegram_link",
            "social_insurance_number",
            "mobile_number",
            "reporting_to",
            "birthday",
            "location",
            "skills",
            "user_certificates",
            "reporting_to",
            "joining_at",
            "job_title",
            "address",
            "user_type",
            "background_color",
            "is_active",
        ]

    def get_user_certificates(self, obj):
        training_courses = get_training_courses_for_a_user(obj.id)
        return TrainingCoursesSerializer(training_courses, many=True).data

    def get_image(self, obj):
        return obj.image.url if obj.image else obj.background_color

    def get_skills(self, obj):
        return UserSkillsSerializer(obj.skills.all(), many=True).data

    def get_reporting_to(self, obj):
        return TeamSerializer(obj.reporting_to.all(), many=True).data

    def get_location(self, obj):
        return OfficeSerializer(obj.location).data


class SupervisorUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user to a supervisor
    """

    user_certificates = SerializerMethodField()
    user_company_properties = SerializerMethodField()
    user_evaluation = SerializerMethodField()
    image = SerializerMethodField()
    skills = SerializerMethodField()
    location = SerializerMethodField()
    reporting_to = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "gender",
            "full_name",
            "image",
            "telegram_link",
            "birthday",
            "location",
            "skills",
            "user_certificates",
            "reporting_to",
            "joining_at",
            "social_insurance_number",
            "team",
            "user_company_properties",
            "mobile_number",
            "user_evaluation",
            "job_title",
            "address",
            "user_type",
            "is_active",
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

    def get_image(self, obj):
        return obj.image.url if obj.image else obj.background_color

    def get_skills(self, obj):
        return UserSkillsSerializer(obj.skills.all(), many=True).data

    def get_reporting_to(self, obj):
        return TeamSerializer(obj.reporting_to.all(), many=True).data

    def get_location(self, obj):
        return OfficeSerializer(obj.location).data


class AdminUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user to an admin
    """

    user_certificates = SerializerMethodField()
    user_company_properties = SerializerMethodField()
    user_evaluation = SerializerMethodField()
    image = SerializerMethodField()
    skills = SerializerMethodField()
    location = SerializerMethodField()
    reporting_to = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "gender",
            "email",
            "full_name",
            "image",
            "telegram_link",
            "birthday",
            "location",
            "skills",
            "user_certificates",
            "reporting_to",
            "joining_at",
            "social_insurance_number",
            "team",
            "user_company_properties",
            "salary",
            "mobile_number",
            "user_evaluation",
            "job_title",
            "address",
            "user_type",
            "is_active",
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

    def get_image(self, obj):
        return obj.image.url if obj.image else obj.background_color

    def get_skills(self, obj):
        return UserSkillsSerializer(obj.skills.all(), many=True).data

    def get_reporting_to(self, obj):
        return TeamSerializer(obj.reporting_to.all(), many=True).data

    def get_location(self, obj):
        return OfficeSerializer(obj.location).data


class SelfUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user to themselves
    """

    user_certificates = SerializerMethodField()
    user_company_properties = SerializerMethodField(read_only=True)
    user_evaluation = SerializerMethodField(read_only=True)
    reporting_to = SerializerMethodField(read_only=True)
    team = CharField(read_only=True)
    salary = JSONField(read_only=True)
    image = SerializerMethodField()
    skills = SerializerMethodField()
    location = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "email",
            "full_name",
            "image",
            "telegram_link",
            "birthday",
            "location",
            "skills",
            "user_certificates",
            "reporting_to",
            "joining_at",
            "social_insurance_number",
            "team",
            "user_company_properties",
            "salary",
            "mobile_number",
            "user_evaluation",
            "job_title",
            "address",
            "user_type",
            "background_color",
            "is_active",
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
        reporting_to = obj.reporting_to.all()
        return TeamSerializer(reporting_to, many=True).data

    def get_image(self, obj):
        return obj.image.url if obj.image else obj.background_color

    def get_skills(self, obj):
        return UserSkillsSerializer(obj.skills.all(), many=True).data

    def get_location(self, obj):
        return OfficeSerializer(obj.location).data


class BaseUserSerializer(ModelSerializer):
    """Implemented to be standered class for multiple usecases."""

    image = SerializerMethodField()
    skills = SerializerMethodField()
    user_certificates = SerializerMethodField()
    location = SerializerMethodField()
    reporting_to = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "first_name",
            "email",
            "image",
            "team",
            "gender",
            "skills",
            "job_title",
            "user_certificates",
            "is_active",
            "telegram_link",
            "reporting_to",
            "location"
        ]
    
    def get_location(self, obj):
        return OfficeSerializer(obj.location).data

    def get_image(self, obj):
        return obj.image.url if obj.image else obj.background_color

    def get_skills(self, obj):
        return UserSkillsSerializer(obj.skills.all(), many=True).data

    def get_user_certificates(self, obj):
        training_courses = get_training_courses_for_a_user(obj.id)
        return TrainingCoursesSerializer(training_courses, many=True).data

    def get_reporting_to(self, obj):
        return BasicUserSerializer(obj.reporting_to, many=True).data

class TeamSerializer(ModelSerializer):
    """Class team serilaizer to return user team leaders and team members."""

    image = SerializerMethodField()
    location = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "image",
            "team",
            "job_title",
            "user_type",
            "mobile_number",
            "address",
            "location",
            "is_active",
            "telegram_link",
        ]

    def get_image(self, obj):
        return obj.image.url if obj.image else obj.background_color

    def get_location(self, obj):
        return OfficeSerializer(obj.location).data


class BasicUserSerializer(ModelSerializer):
    """Implemented to be standered class for multiple usecases."""

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "is_active",
        ]


class UpdateUserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user to themselves
    """

    user_certificates = SerializerMethodField()
    user_company_properties = SerializerMethodField(read_only=True)
    user_evaluation = SerializerMethodField(read_only=True)
    reporting_to = SerializerMethodField(read_only=True)
    joining_at = DateField(read_only=True)
    team = CharField(read_only=True)
    salary = JSONField(read_only=True)
    image = Base64ImageField(
        max_length=None,
        use_url=True,
        required=False,
        allow_null=True,
    )
    skills = SerializerMethodField()
    location = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "email",
            "full_name",
            "image",
            "telegram_link",
            "birthday",
            "location",
            "skills",
            "user_certificates",
            "reporting_to",
            "joining_at",
            "social_insurance_number",
            "team",
            "user_company_properties",
            "salary",
            "mobile_number",
            "user_evaluation",
            "job_title",
            "address",
            "user_type",
            "background_color",
            "is_active",
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
        reporting_to = obj.reporting_to.all()
        return TeamSerializer(reporting_to, many=True).data

    def get_skills(self, obj):
        return UserSkillsSerializer(obj.skills.all(), many=True).data

    def get_location(self, obj):
        return OfficeSerializer(obj.location).data
